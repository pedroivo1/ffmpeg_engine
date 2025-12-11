from functools import wraps
from datetime import timedelta
import re

def validate_choices(choices: list | tuple | set):
    """
    Validate if the input value is within the allowed choices.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if value not in choices:
                raise ValueError(
                    f"Value {repr(value)} is not allowed. "
                    f"Valid options: {choices}")
            return func(self, value)
        return wrapper
    return decorator


def time_to_string():
    """
    Converts time inputs into FFmpeg-compatible string formats.
    
    - timedelta: Converts to "HH:MM:SS.mmm" (Timestamp format)
    - int/float: Converts to "123.456" (Seconds format)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):

            if not isinstance(value, (timedelta, float, int)):
                raise TypeError(
                    f"Time must be timedelta, float, or int, got {type(value).__name__}"
                )

            if isinstance(value, timedelta):
                total_seconds = value.total_seconds()
                
                if total_seconds < 0:
                    raise ValueError(f"Time value cannot be negative")

                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                time_str = f"{int(hours):02}:{int(minutes):02}:{seconds:06.3f}"

            else:
                seconds_val = float(value)
                if seconds_val < 0:
                    raise ValueError(f"Time value cannot be negative")
                
                time_str = f"{seconds_val:.3f}"

            return func(self, time_str)
        return wrapper
    return decorator


def validate_int(min_value: int | None = None, max_value: int | None = None):
    """
    Validate integer inputs, ensuring type correctness and 
    optional range constraints (min/max).
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if not isinstance(value, int):
                raise TypeError(
                    f"{func.__name__} must be int, got {type(value).__name__}"
                )
            
            if min_value is not None and value < min_value:
                raise ValueError(
                    f"{func.__name__} must be >= {min_value}, got {value}"
                )

            if max_value is not None and value > max_value:
                raise ValueError(
                    f"{func.__name__} must be <= {max_value}, got {value}"
                )
            
            return func(self, value)
        return wrapper
    return decorator


def convert_sample_rate():
    """
    Validate and convert sample rate inputs.
    
    Accepts:
    - int/float: 44100, 48000.0
    - str: "44100", "44.1k", "48k"
    
    Converts everything to a positive integer (Hz).
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):

            if not isinstance(value, (int, float, str)):
                raise TypeError(
                    f"sample_rate must be int, float or str, got {type(value).__name__}"
                )
            
            final_value = None
            try:
                if isinstance(value, (int, float)):
                    final_value = int(value)
                else:
                    # Lógica de String (ex: "44k", "44.1k", "48000")
                    s_val = value.lower().strip()
                    if s_val.endswith("k"):
                        number_part = float(s_val[:-1])
                        final_value = int(number_part * 1000)
                    else:
                        final_value = int(float(s_val))
            except ValueError:
                raise ValueError(f"Invalid sample_rate string format: '{value}'")

            if final_value <= 0:
                raise ValueError(f"{func.__name__} must be greater than 0")
            
            return func(self, final_value)
        return wrapper
    return decorator


def validate_positive_number():
    """Valida se o número (int ou float) é maior que zero."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if not isinstance(value, (int, float)):
                raise TypeError(f"{func.__name__} must be int or float, got {type(value).__name__}")
            if value <= 0:
                raise ValueError(f"{func.__name__} must be > 0, got {value}")
            return func(self, value)
        return wrapper
    return decorator

def validate_video_size(aliases: set):
    """Valida tamanho de vídeo: aceita aliases (ex: 'hd1080') ou formato 'WxH'."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if not isinstance(value, str) or not value:
                raise ValueError(f"Size must be a non-empty string.")
            
            s_val = value.lower().strip()
            is_wxh = re.match(r"^\d+x\d+$", s_val)
            is_alias = s_val in aliases

            if not (is_wxh or is_alias):
                raise ValueError(f"Invalid size format: '{value}'. Must be 'WxH' or a valid alias.")
            
            return func(self, s_val)
        return wrapper
    return decorator

def validate_number(min_value: float | int | None = None, max_value: float | int | None = None):
    """
    Valida números (int ou float), com limites opcionais.
    Útil para qscale ou framerate que podem ser float.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if not isinstance(value, (int, float)):
                raise TypeError(
                    f"{func.__name__} must be int or float, got {type(value).__name__}"
                )
            
            if min_value is not None and value < min_value:
                raise ValueError(
                    f"{func.__name__} must be >= {min_value}, got {value}"
                )

            if max_value is not None and value > max_value:
                raise ValueError(
                    f"{func.__name__} must be <= {max_value}, got {value}"
                )
            
            return func(self, value)
        return wrapper
    return decorator
