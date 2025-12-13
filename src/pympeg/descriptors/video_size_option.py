import re
from .base_option import BaseOption


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

        raise ValueError(
            f"Invalid video size: '{value}'. Must be in valid list or WxH format."
        )
