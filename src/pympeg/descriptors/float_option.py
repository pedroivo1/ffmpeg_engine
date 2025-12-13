from .base_option import BaseOption


class FloatOption(BaseOption):

    def __init__(
        self,
        flag: str,
        min_val: float | int | None = None,
        max_val: float | int | None = None
    ) -> None:

        super().__init__(flag)
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, value: object) -> float | int:
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"{self.name} must be float or int, got {type(value).__name__}"
            )

        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"{self.name} must be >= {self.min_val}")

        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"{self.name} must be <= {self.max_val}")

        return value
