from abc import ABC
from .descriptors import BaseOption

class Options(ABC):
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Opção inválida: '{key}'")

    def generate_command_args(self) -> list[str]:
        args = []
        for attr_name, attr_value in self.__class__.__dict__.items():
            
            if isinstance(attr_value, BaseOption):
                value = getattr(self, attr_name)
                
                if value is not None:
                    args.extend(attr_value.to_args(value))
        
        return args
