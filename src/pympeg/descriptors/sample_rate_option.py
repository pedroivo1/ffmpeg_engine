from .base_option import BaseOption


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
