from functools import wraps

def validate_choices(choices: list | tuple | set):
    """
    Decorator to validate if the input value is within the allowed choices.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            
            if value not in choices:
                raise ValueError(
                    f"Value '{value}' is not allowed. "
                    f"Valid options: {sorted(choices)}"
                )
            
            return func(self, value)
        return wrapper
    return decorator
