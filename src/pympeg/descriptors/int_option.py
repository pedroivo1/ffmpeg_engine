from .base_option import BaseOption


class IntOption(BaseOption):

    def __init__(
        self,
        flag: str,
        min_val: int | None = None,
        max_val: int | None = None
    ) -> None:

        super().__init__(flag)
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, value: object) -> int:
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(
                f"{self.name} must be int, got {type(value).__name__}"
            )

        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"{self.name} must be >= {self.min_val}")

        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"{self.name} must be <= {self.max_val}")

        return value
