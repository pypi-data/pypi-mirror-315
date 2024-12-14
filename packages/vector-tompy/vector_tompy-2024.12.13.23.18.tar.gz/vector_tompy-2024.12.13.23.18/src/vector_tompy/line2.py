from dataclasses import dataclass
from decimal import Decimal
from typing import Self

from .exceptions import NoLinesIntersectionError, UnexpectedUnpredictableError
from .vector2 import Vector2, Vector2Injector


@dataclass
class Line2:
    point0: Vector2
    point1: Vector2

    def intersection(self, other: Self) -> Vector2:
        # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
        l0p0: Vector2 = self.point0
        l0p1: Vector2 = self.point1
        l1p0: Vector2 = other.point0
        l1p1: Vector2 = other.point1
        denominator = (l0p0.x - l0p1.x) * (l1p0.y - l1p1.y) - (l0p0.y - l0p1.y) * (l1p0.x - l1p1.x)

        if denominator != Decimal("0"):
            x: Decimal = ((l0p0.x * l0p1.y - l0p0.y * l0p1.x) * (l1p0.x - l1p1.x) -
                          (l0p0.x - l0p1.x) * (l1p0.x * l1p1.y - l1p0.y * l1p1.x)) / denominator
            y: Decimal = ((l0p0.x * l0p1.y - l0p0.y * l0p1.x) * (l1p0.y - l1p1.y) -
                          (l0p0.y - l0p1.y) * (l1p0.x * l1p1.y - l1p0.y * l1p1.x)) / denominator
            intersection_: Vector2 = Vector2Injector.from_decimal(x=x, y=y)
        elif denominator == Decimal("0"):
            raise NoLinesIntersectionError(f"Lines are parallel as denominator is 0 "
                                           f"and thus does not have a single intersection.")
        else:
            raise UnexpectedUnpredictableError(f"The comparison of two values ('{0}', '{denominator}') "
                                               f"just went extremely unexpectedly wrong.")

        return intersection_


class Line2Injector:
    @staticmethod
    def from_vectors(point0: Vector2, point1: Vector2) -> Line2:
        line: Line2 = Line2(point0=point0, point1=point1)
        return line

    @staticmethod
    def from_base_scalar(base: Vector2, scalar: Vector2) -> Line2:
        point0: Vector2 = base
        point1: Vector2 = base + scalar
        line: Line2 = Line2(point0=point0, point1=point1)
        return line
