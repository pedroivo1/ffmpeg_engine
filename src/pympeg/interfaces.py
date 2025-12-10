from abc import ABC, abstractmethod
from datetime import timedelta
import logging
from functools import wraps

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Options(ABC):
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
    
    @staticmethod
    def valida_lista(permitidos, mensage: str = None):
        def decorador(func):
            @wraps(func)
            def wrapper(self, value):
                if value not in permitidos:
                    if mensage:
                        raise ValueError(mensage)
                    else:
                        raise ValueError(
                            f"Valor '{value}' não permitido. "
                            f"Valores válidos: {sorted(permitidos)}"
                        )
                return func(self, value)
            return wrapper
        return decorador

    def _log_invalid_value(self, attr_name: str, value: str | int | float | None):
        class_name = self.__class__.__name__
        logger.error(
            f"Invalid value '{value}' received for '{attr_name}' on {class_name}."
        )




# def conflicts_with(other_param: str):
#     """Valida se dois parâmetros não estão definidos simultaneamente"""
#     def decorator(func):
#         def wrapper(self, value):
#             other_value = getattr(self, other_param, None)
#             if other_value is not None:
#                 raise ValueError(
#                     f"Conflito: não pode definir {func.__name__} "
#                     f"quando {other_param}={other_value} já está definido"
#                 )
#             return func(self, value)
#         return wrapper
#     return decorator
