from .base_option import BaseOption
from datetime import timedelta


class TimeOption(BaseOption):

    def validate(self, value: object) -> str:
        if not isinstance(value, (timedelta, int, float)):
            raise TypeError(
                f"Time must be timedelta, int or float. Got {type(value).__name__}"
            )

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
