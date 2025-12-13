from datetime import timedelta
import re

class BaseOption:
    def __init__(self, flag: str) -> None:
        self.flag = flag
        self.name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: object, owner: type | None = None) -> object | None:
        if instance is None: return self
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance: object, value: object) -> None:
        if value is None:
            instance.__dict__.pop(self.name, None)
        else:
            instance.__dict__[self.name] = self.validate(value)

    def __delete__(self, instance: object) -> None:
        instance.__dict__.pop(self.name, None)

    def validate(self, value: object) -> object:
        return value

    def to_args(self, value: object) -> list[str]:
        return [self.flag, str(value)]


class ChoiceOption(BaseOption):
    def __init__(self, flag: str, choices: set[str]) -> None:
        super().__init__(flag)
        self.choices = choices

    def validate(self, value: object) -> str:
        s_val = str(value)
        if s_val not in self.choices:
            raise ValueError(f"Value '{value}' not allowed. Valid: {self.choices}")
        return s_val


class BoolOption(BaseOption):
    def __init__(self, true_flag: str | None = None, false_flag: str | None = None) -> None:
        # BoolOption não tem uma 'flag' única padrão, então passamos vazia pro pai
        super().__init__("") 
        self.true_flag = true_flag
        self.false_flag = false_flag

    def validate(self, value: object) -> bool:
        if not isinstance(value, bool):
            raise TypeError(f"{self.name} must be bool")
        return value

    def to_args(self, value: object) -> list[str]:
        if value is True and self.true_flag:
            return [self.true_flag]
        if value is False and self.false_flag:
            return [self.false_flag]
        return []


class IntOption(BaseOption):
    def __init__(self, flag: str, min_val: int | None = None, max_val: int | None = None) -> None:
        super().__init__(flag)
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, value: object) -> int:
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(f"{self.name} must be int, got {type(value).__name__}")
        
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"{self.name} must be >= {self.min_val}")
        
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"{self.name} must be <= {self.max_val}")
            
        return value


class FloatOption(BaseOption):
    def __init__(self, flag: str, min_val: float | int | None = None, max_val: float | int | None = None) -> None:
        super().__init__(flag)
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, value: object) -> float | int:
        if not isinstance(value, (float, int)):
            raise TypeError(f"{self.name} must be float or int, got {type(value).__name__}")

        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"{self.name} must be >= {self.min_val}")

        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"{self.name} must be <= {self.max_val}")

        return value


class TimeOption(BaseOption):
    def validate(self, value: object) -> str:
        if not isinstance(value, (timedelta, int, float)):
            raise TypeError(f"Time must be timedelta, int or float. Got {type(value).__name__}")

        if isinstance(value, timedelta):
            total_seconds = value.total_seconds()
            if total_seconds < 0:
                raise ValueError("Time cannot be negative")
            
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f'{int(hours):02}:{int(minutes):02}:{seconds:06.3f}'
        
        seconds_val = float(value)
        if seconds_val < 0:
            raise ValueError("Time cannot be negative")
        
        return f'{seconds_val:.3f}'


class SampleRateOption(BaseOption):
    def validate(self, value: object) -> int:
        if not isinstance(value, (int, float, str)):
            raise TypeError(f"{self.name} must be int, float or str")
        
        final_value = None
        try:
            if isinstance(value, (int, float)):
                final_value = int(value)
            else:
                s_val = value.lower().strip()
                if s_val.endswith('k'):
                    number_part = float(s_val[:-1])
                    final_value = int(number_part * 1000)
                else:
                    final_value = int(float(s_val))
        except ValueError:
            raise ValueError(f"Invalid sample_rate format: '{value}'")

        if final_value <= 0:
            raise ValueError(f"{self.name} must be positive")
            
        return final_value


class VideoSizeOption(BaseOption):
    def __init__(self, flag: str, valid_sizes: set[str]) -> None:
        super().__init__(flag)
        self.valid_sizes = valid_sizes

    def validate(self, value: object) -> str:
        s_val = str(value).lower()
        
        if s_val in self.valid_sizes:
            return s_val
            
        if re.match(r'^\d+x\d+$', s_val):
            return s_val
            
        raise ValueError(f"Invalid video size: '{value}'. Must be in valid list or WxH format.")


class BitrateOption(BaseOption):
    def validate(self, value: object) -> int:
        if not isinstance(value, (int, str)):
            raise TypeError(f"{self.name} must be int or str")
        
        if isinstance(value, int):
            if value <= 0:
                raise ValueError(f"{self.name} must be positive")
            return value
            
        s_val = value.strip()
        multiplier = 1
        if s_val.lower().endswith('k'):
            multiplier = 1000
            s_val = s_val[:-1]
        elif s_val.lower().endswith('m'):
            multiplier = 1000000
            s_val = s_val[:-1]
            
        try:
            final_val = int(float(s_val) * multiplier)
            if final_val <= 0:
                raise ValueError
            return final_val
        except ValueError:
            raise ValueError(f"Invalid bitrate format: '{value}'")


class DictOption(BaseOption):
    def validate(self, value: object) -> dict[str, str]:
        if not isinstance(value, dict):
            raise TypeError(f"{self.name} must be dict")
        return value

    def to_args(self, value: object) -> list[str]:
        args = []
        if isinstance(value, dict):
            for k, v in value.items():
                if k and v: # Ignora chaves/valores vazios
                    args.extend([self.flag, f"{k}={v}"])
        return args