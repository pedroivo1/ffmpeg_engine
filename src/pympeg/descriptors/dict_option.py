from .base_option import BaseOption


class DictOption(BaseOption):

    def validate(self, value: object) -> dict[str, str]:
        if not isinstance(value, dict):
            raise TypeError(f"{self.name} must be dict")
        return value

    def to_args(self, value: object) -> list[str]:
        args = []
        if isinstance(value, dict):
            for k, v in value.items():
                if k and v:
                    args.extend([self.flag, f"{k}={v}"])
        return args
