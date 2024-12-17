from lib import trace_loop
import time
from opentelemetry import trace

if __name__ == "__main__":
    tr = trace.get_tracer(__name__)
    with tr.start_as_current_span("sp"):
        time.sleep(0.1)

class MyOtelTest:
    def requirements(self):
        return "opentelemetry-distro", "opentelemetry-exporter-otlp-proto-grpc"

    def environment_variables(self):
        return {
            "OTEL_SERVICE_NAME": "svcn",
            "OTEL_PYTHON_DISABLED_INSTRUMENTATIONS": "system_metrics",
        }

    def wrapper_command(self):
        return "opentelemetry-instrument"

    def on_start(self):
        return None

    def on_stop(self, telemetry, stdout: str, stderr: str, returncode: int) -> None:
        pass

    def is_http(self):
        return False
