from abc import ABC, abstractmethod
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Options(ABC):

    def _log_invalid_value(self, attr_name: str, value: str | int | float | None):
        class_name = self.__class__.__name__
        logger.error(
            f"Invalid value '{value}' received for '{attr_name}' on {class_name}."
        )

    @abstractmethod
    def generate_command_args(self) -> list:
        pass

    def time_to_str(self, time, limit) -> str:
        if isinstance(time, timedelta):
            total_seconds = time.total_seconds()
            H, R = divmod(total_seconds, 3600)
            M, S = divmod(R, 60)
            return f"{int(H):02}:{int(M):02}:{S:06.3f}"
        elif isinstance(time, (float, int)) and time >= limit:
            return f"{time:.3f}"

        return None
