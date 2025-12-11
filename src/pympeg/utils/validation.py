from functools import wraps
from datetime import timedelta

def validate_choices(choices: list | tuple | set):
    """
    Decorator to validate if the input value is within the allowed choices.
    """
    valid_options_str = ", ".join(sorted(map(repr, choices)))

    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if value not in choices:
                raise ValueError(
                    f"Value {repr(value)} is not allowed. "
                    f"Valid options: {valid_options_str}"
                )
            return func(self, value)
        return wrapper
    return decorator


def time_to_string():
    """
    Decorator that converts time inputs into FFmpeg-compatible string formats.
    
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
                    raise ValueError(f"Time value {seconds_val}s cannot be negative")
                
                time_str = f"{seconds_val:.3f}"
            
            return func(self, time_str)
        return wrapper
    return decorator
