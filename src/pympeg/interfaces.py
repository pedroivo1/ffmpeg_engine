from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Options(ABC):
    @abstractmethod
    def generate_command_args(self) -> list:
        pass



# def conflicts_with(other_param: str):
#     '''Valida se dois parâmetros não estão definidos simultaneamente'''
#     def decorator(func):
#         def wrapper(self, value):
#             other_value = getattr(self, other_param, None)
#             if other_value is not None:
#                 raise ValueError(
#                     f'Conflito: não pode definir {func.__name__} '
#                     f'quando {other_param}={other_value} já está definido'
#                 )
#             return func(self, value)
#         return wrapper
#     return decorator
