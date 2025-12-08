from abc import ABC, abstractmethod
import logging

# 1. Configura o Logger NESTE arquivo
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class Options(ABC):

    def _log_invalid_value(self, attr_name: str, value: str | int | float | None):
        class_name = self.__class__.__name__
        logger.error(f"Invalid value '{value}' received for '{attr_name}' on {class_name}.")

    @abstractmethod
    def generate_command_args(self) -> list:
        pass
