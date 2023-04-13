from __future__ import annotations
from math import sqrt
from random import randrange, random

class VectorError(Exception): ...

class Vec2:
    x: int
    y: int

    @staticmethod 
    def error(__error__: str):
        raise VectorError(__error__)

    @staticmethod
    def random(upper_bound: float) -> Vec2:
        return Vec2(
            random() * upper_bound + 1,
            random() * upper_bound + 1,
        )

    def __init__(self, x: int, y: int = None) -> None:
        self.x = x
        self.y = y

        if y == None:
            self.y = self.x
    
    def __add__(self, other: Vec2):
        if not isinstance(other, Vec2):
            Vec2.error("Attempted to add non-vector value to vector.")

        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2):
        if not isinstance(other, Vec2):
            Vec2.error("Attempted to subtract non-vector value from vector.")

        return self.distance(other)

    def __mul__(self, other: Vec2):
        if isinstance(other, int) or isinstance(other, float):
            return Vec2(self.x * other, self.y * other)
        elif isinstance(other, Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        else:
            Vec2.error("Attempted to multiply vector by non-int and non-vector value.")
    
    def __div__(self, other: Vec2):
        if isinstance(other, int) or isinstance(other, float):
            return self.__mul__(1/other)
        elif isinstance(other, Vec2):
            return self.__mul__(Vec2(1/other.x, 1/other.y))
        else:
            Vec2.error("Attempted to divide vector by non-int and non-vector value.")
    
    def __repr__(self) -> str:
        return f"[{self.x}, {self.y}]"
    
    def length(self) -> float:
        return sqrt((self.x*self.x) + (self.y*self.y))

    def distance(self, other: Vec2) -> float:
        return sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2))

    def normalised(self) -> Vec2:
        return self / self.length()