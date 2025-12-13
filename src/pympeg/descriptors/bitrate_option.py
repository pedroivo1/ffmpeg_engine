from .base_option import BaseOption


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
