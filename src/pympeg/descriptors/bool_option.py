from .base_option import BaseOption


class BoolOption(BaseOption):

    def __init__(
        self,
        true_flag: str | None = None,
        false_flag: str | None = None
    ) -> None:

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
