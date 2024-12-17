import functools
import logging
import traceback
from typing import Callable
from uuid import uuid4

from flask import Flask, g, got_request_exception, request
from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.utils import _get_opentelemetry_values
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider, sampling
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)
from opentelemetry.trace.status import Status, StatusCode
from opentelemetry.util.types import Attributes


def exception_handler(exc: Exception):
    span = trace.get_current_span()
    span.record_exception(exc)
    span.set_status(Status(StatusCode.ERROR, str(exc)))


def get_trace_id_from_span(span: trace.Span) -> str:
    return hex(span.get_span_context().trace_id)[2::].zfill(32)


def setup_inject_trace_id(app: Flask):
    def inject_trace_id_to_g_object():
        g.trace_id = get_trace_id_from_span(trace.get_current_span())
        g.trace_header = _get_opentelemetry_values().get("traceparent")

    def inject_trace_id_in_templates():
        return dict(trace_id=g.trace_id)

    app.before_request(inject_trace_id_to_g_object)
    app.context_processor(inject_trace_id_in_templates)


def setup_inject_parent_trace_id(app: Flask):
    def inject_parent_trace_id_to_request_environ():
        request.environ["HTTP_TRACEPARENT"] = request.args.get("trace_parent", None)

    app.before_request(inject_parent_trace_id_to_request_environ)


def setup_inject_session_id(app: Flask):
    session_id_cookie_name = f"{app.name}-session-id"

    def check_or_create_session_id():
        session_id = request.cookies.get(session_id_cookie_name)

        if not session_id:
            session_id = str(uuid4())
        g.session_id = session_id

        trace.get_current_span().set_attribute("session_id", session_id)

    def set_session_id_cookie(response):
        if hasattr(g, "session_id"):
            # Set the new SessionID cookie in the response
            response.set_cookie(session_id_cookie_name, g.session_id)
        return response

    def inject_session_id_in_templates():
        return dict(session_id=g.session_id)

    app.before_request(check_or_create_session_id)
    app.after_request(set_session_id_cookie)
    app.context_processor(inject_session_id_in_templates)


def setup_jinja2_instrumentation():
    from opentelemetry.instrumentation.jinja2 import Jinja2Instrumentor

    Jinja2Instrumentor().instrument()


def setup_psycopg_instrumentation():
    from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor

    PsycopgInstrumentor().instrument()


def setup_flask_instrumentation(app: Flask):
    # parent trace id injection
    setup_inject_parent_trace_id(app)

    # auto instrumentation
    FlaskInstrumentor().instrument_app(app)

    # trace id injection
    setup_inject_trace_id(app)

    # error handling
    # app.register_error_handler(Exception, exception_handler)

    # session id injection
    setup_inject_session_id(app)

    @app.teardown_request
    def log_exception(exc):
        if exc:
            app.logger.error("Unhandled Exception", exc_info=exc)

    @got_request_exception.connect_via(app)
    def log_flask_exception(sender, exception, **extra):
        app.logger.exception(traceback.format_exc(), exc_info=exception)


def setup_logging_instrumentation(service_name: str):
    LoggingInstrumentor().instrument()

    logger_provider = LoggerProvider(
        resource=Resource.create(
            {
                "service.name": service_name,
            }
        ),
    )
    set_logger_provider(logger_provider)

    log_exporter = OTLPLogExporter(insecure=True)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    handler = LoggingHandler(logger_provider=logger_provider)

    logging.getLogger().setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    logging.getLogger().addHandler(stream_handler)
    logging.getLogger().addHandler(handler)


def setup_tracing_instrumentation(service_name: str):
    trace_exporter = OTLPSpanExporter(insecure=True)
    trace.set_tracer_provider(
        TracerProvider(resource=Resource(attributes={"service.name": service_name}))
    )
    tracer_provider = trace.get_tracer_provider()
    tracer_provider.sampler = sampling.StaticSampler(
        sampling.Decision.RECORD_AND_SAMPLE
    )
    tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))


def setup_instrumentation(app: Flask, service_name: str):
    setup_logging_instrumentation(service_name=service_name)
    setup_tracing_instrumentation(service_name=service_name)

    # Additional instrumentation
    setup_flask_instrumentation(app)
    setup_jinja2_instrumentation()
    setup_psycopg_instrumentation()


def trace_func(
    func: Callable | None = None,
    /,
    name: str | None = None,
    attributes: Attributes | None = None,
    attribute_collector: Callable | None = None,
):
    def trace_func_func_step(func: Callable | None = None) -> Callable:
        @functools.wraps(func)
        def trace_func_call_wrap_step(*args, **kwargs):
            tracer = trace.get_tracer(func.__module__)
            with tracer.start_as_current_span(
                name or func.__name__, attributes=attributes
            ) as span:
                result = func(*args, **kwargs)
                if attribute_collector is not None:
                    collected_attributes = attribute_collector(result, *args, **kwargs)
                    span.set_attributes(collected_attributes)
                return result

        return trace_func_call_wrap_step

    if func is None:
        return trace_func_func_step
    else:
        return trace_func_func_step(func)
