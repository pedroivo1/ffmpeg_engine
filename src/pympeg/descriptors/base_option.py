class BaseOption:

    def __init__(self, flag: str) -> None:
        self.flag = flag
        self.name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(
        self,
        instance: object,
        owner: type | None = None
    ) -> object | None:
    
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
