import math


class ShowAccess:
    def __set_name__(self, owner, name):
        self.name = name  # Запоминаем имя атрибута

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = instance.__dict__.get(self.name)
        print(f"Get {self.name} = {value}")
        return value

    def __set__(self, instance, value):
        print(f"Set {self.name} = {value}")
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        value = instance.__dict__.get(self.name)
        print(f"Delete {self.name} = {value}")
        del instance.__dict__[self.name]


class DebugObject:
    pass


class Circle(DebugObject):
    radius = ShowAccess()

    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return math.pi * self.radius ** 2


# Пример использования
c = Circle(100)
_ = c.area

del c.radius
