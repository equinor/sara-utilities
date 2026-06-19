import logging

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from sara_utilities.config.settings import settings


def setup_open_telemetry() -> trace.Tracer:
    service_name = settings.OTEL_SERVICE_NAME

    base_ep = settings.OTEL_EXPORTER_OTLP_ENDPOINT
    traces_endpoint = base_ep.rstrip("/") + "/v1/traces"
    logs_endpoint = base_ep.rstrip("/") + "/v1/logs"

    resource = Resource.create({"service.name": service_name})

    # --- Traces ---
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=traces_endpoint))
    )
    trace.set_tracer_provider(tracer_provider)
    tracer = trace.get_tracer(service_name)

    # --- Logs ---
    log_provider = LoggerProvider(resource=resource)
    log_provider.add_log_record_processor(
        BatchLogRecordProcessor(OTLPLogExporter(endpoint=logs_endpoint))
    )

    handler = LoggingHandler(level=logging.INFO, logger_provider=log_provider)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)

    return tracer
