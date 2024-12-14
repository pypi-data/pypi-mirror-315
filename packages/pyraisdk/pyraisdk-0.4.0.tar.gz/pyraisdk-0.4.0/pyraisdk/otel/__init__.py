import logging
import os
import signal
import threading
from typing import Optional
from opentelemetry.metrics import set_meter_provider, get_meter_provider
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators import composite
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.baggage.propagation import W3CBaggagePropagator
from opentelemetry.sdk.environment_variables import OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE
from opentelemetry.sdk.metrics import MeterProvider, Counter, UpDownCounter, Histogram, ObservableCounter, ObservableUpDownCounter, ObservableGauge
from opentelemetry.sdk.metrics.export import AggregationTemporality, PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_NAMESPACE, SERVICE_VERSION, SERVICE_INSTANCE_ID, HOST_NAME
from opentelemetry.semconv.metrics import MetricInstruments

from .auth import AuthClient
from .config import OtelConfig
from .customExporter import CustomOTLPMetricExporter

ATTR_REGION = "Region"
ATTR_ENVIRONMENT = "Envrironment"
ATTR_INSTANCE = "Instance"
ATTR_TRAFFICTYPE = "TrafficType"

logger = logging.getLogger("otel")
stop_evt = threading.Event()

def initialize(
    service_name: Optional[str] = None, 
    service_namespace: Optional[str] = None, 
    service_version: Optional[str]=None, 
    service_instance_id: Optional[str]=None,
    host_name: Optional[str]=None
):
    config = OtelConfig()
    if not config.is_active():
        logger.warning(f"Not configuring OTEL due to missing configuration")
        return

    if OTEL_EXPORTER_OTLP_ENDPOINT not in  os.environ:
        os.environ.setdefault(OTEL_EXPORTER_OTLP_ENDPOINT, config.endpoint)

    if OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE not in os.environ:
        os.environ.setdefault(OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE, "DELTA")

    res = Resource(
            attributes={
                SERVICE_NAME: service_name if service_name != None else os.environ.get("ENDPOINT_NAME", ""),
                SERVICE_NAMESPACE: service_namespace if service_namespace != None else os.environ.get("MODEL_NAME", ""),
                SERVICE_VERSION: service_version if service_version != None else os.environ.get("ENDPOINT_VERSION", ""),
                SERVICE_INSTANCE_ID: service_instance_id if service_instance_id != None else f"{os.environ.get('MODEL_NAME', '')}|{os.environ.get('ENDPOINT_NAME', '')}|{os.environ.get('ENDPOINT_VERSION', '')}|{os.environ.get('HOSTNAME', '')}" ,
                ATTR_REGION: config.region,
                ATTR_ENVIRONMENT: config.environment,
                HOST_NAME: host_name if host_name != None else os.environ.get("HOSTNAME", ""),
                ATTR_INSTANCE: os.environ.get("INSTANCE", ""),
                ATTR_TRAFFICTYPE: os.environ.get("OPEN_TELEMETRY_SESSION_TRAFFIC_TYPE", "Unknown")
            },
            schema_url=MetricInstruments.SCHEMA_URL
        )
    auth_client = AuthClient(config, stop_evt)
    try:
        # attempt getting the token to avoid configuring OTEL in case of errors
        auth_client.get_token()
        set_global_textmap(composite.CompositePropagator([TraceContextTextMapPropagator(), W3CBaggagePropagator()]))

        exporter = CustomOTLPMetricExporter(auth_client)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis= 30 * 1000)
        meter_provider = MeterProvider(metric_readers=[reader], resource=res)
        set_meter_provider(meter_provider) 
        
        def handle_signal(signal_number, frame):
            logger.warning(f"Received signal: {signal_number}")
            shutdown()

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)
    except:
        stop_evt.set()
        logger.error(f"Skipping OTEL due to error", exc_info=True)

def shutdown():
    if not stop_evt.is_set():
        logger.warning(f"Shutting down OTEL")
        stop_evt.set()
        try:
            meter_provider = get_meter_provider()
            if hasattr(meter_provider, "shutdown") and callable(meter_provider.shutdown):
                meter_provider.shutdown() # this will internally shutdown the exporter, reader and provider
        except:
            # swallow errors during shutdown to avoid breaking the main process
            logger.error("Error during meter provider shutdown", exc_info=True)
            return