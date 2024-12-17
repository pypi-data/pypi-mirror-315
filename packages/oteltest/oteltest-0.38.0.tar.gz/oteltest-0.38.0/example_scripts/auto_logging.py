import logging
from typing import Mapping, Optional, Sequence


def main():
    logger = logging.getLogger(__name__)
    logger.warning("This is a warning message")


if __name__ == '__main__':
    main()



class LoggingOtelTest:
    def environment_variables(self) -> Mapping[str, str]:
        return {
            "OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED": "true",
            "OTEL_LOGS_EXPORTER": "otlp",
        }

    def requirements(self) -> Sequence[str]:
        return ("opentelemetry-distro[otlp]",)

    def wrapper_command(self) -> str:
        return "opentelemetry-instrument"

    def is_http(self) -> bool:
        return False

    def on_start(self) -> Optional[float]:
        pass

    def on_stop(self, tel, stdout: str, stderr: str, returncode: int) -> None:
        pass

