from dataclasses import dataclass
from typing import Self


@dataclass
class Point:
    x: int = 0
    y: int = 0

    @property
    def decoding(self):
        return self.x, self.y

    def move(self, value: int):
        self.x += value
        self.y += value

    def __str__(self):
        return F'<{self.x},{self.y}>'

    def __mul__(self, other: int | float) -> Self:
        """:return Point with scaler x and y by other value"""
        if isinstance(other, (int, float)):
            return Point(int(self.x*other), int(self.y*other))
        else:
            ValueError(F"got unsupport type: {other}, expected int or float")

    def __sub__(self, other: Self) -> Self:
        return self.__class__(
            self.x - other.x,
            self.y - other.y)

    def __add__(self, other) -> Self:
        return self.__class__(
            self.x + other.x,
            self.y + other.y)

    def __floordiv__(self, other: int):
        return self.__class__(
            self.x // other,
            self.y // other)

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise StopIteration
    #
    # def __iter__(self):
    #     return iter((self.x, self.y))


@dataclass
class Box:
    x1: int
    y1: int
    x2: int
    y2: int

    def __iter__(self):
        return iter((self.x1, self.y1, self.x2, self.y2))
