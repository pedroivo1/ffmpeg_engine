from .base_option import BaseOption


class ChoiceOption(BaseOption):

    def __init__(self, flag: str, choices: set[str]) -> None:
        super().__init__(flag)
        self.choices = choices

    def validate(self, value: object) -> str:
        s_val = str(value)
        if s_val not in self.choices:
            raise ValueError(f"Value '{value}' not allowed. Valid: {self.choices}")
        return s_val
