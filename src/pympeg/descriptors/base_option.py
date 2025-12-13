class BaseOption:
    def __init__(self, flag: str) -> None:
        self.flag = flag
        self.name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: object, owner: type | None = None) -> object | None:
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance: object, value: object) -> None:
        if value is None:
            instance.__dict__.pop(self.name, None)
        else:
            validated_value = self.validate(value)
            instance.__dict__[self.name] = validated_value
