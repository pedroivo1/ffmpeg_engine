from abc import ABC, abstractmethod

class MediaFlags(ABC):
    @abstractmethod
    def generate_command_args(self) -> list:
        pass