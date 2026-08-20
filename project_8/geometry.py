"""Integer geometry (points and rectangles) for tree mapping."""
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __add__(self, other) -> "Point":
        assert isinstance(other, Point)
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> "Point":
        assert isinstance(other, Point)
        return Point(self.x + other.x, self.y + other.y)


class Rect:
    """Rectangle with integer coordinates defined by lower left and upper right corners"""
    def __init__(self, lower_left: Point, upper_right: Point):
        self.ll = lower_left
        self.ur = upper_right

    def __str__(self):
        return f"Rect({self.ll}, {self.ur})"

    def height(self) -> int:
        return self.ur.y - self.ll.y

    def width(self) -> int:
        return self.ur.x - self.ll.x

    def split(self, fraction: float) -> tuple["Rect", "Rect"]:
        """Returns two sub-rectangles that together constitute
        this rectangle, with ratio of first to second approximately 'fraction'
        (subject to rounding error).
        """
        if self.height() > self.width():
            frac_height = int(self.height() * fraction)
            bottom = Rect(self.ll, Point(self.ur.x, self.ll.y + frac_height))
            top = Rect(Point(self.ll.x, self.ll.y + frac_height), self.ur)
            log.debug(f"Splitting {self} vertically into {bottom}, {top}")
            return bottom, top
        else:
            frac_width = int(self.width() * fraction)
            left = Rect(self.ll, Point(self.ll.x + frac_width, self.ur.y))
            right = Rect(Point(self.ll.x + frac_width, self.ll.y), self.ur)
            log.debug(f"Splitting {self} horizontally into {left}, {right}")
            return left, right






