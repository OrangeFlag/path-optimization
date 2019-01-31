from math import pi, sin, cos

from shapely.geometry import LineString, Point, Polygon


class Line(LineString):
    def __init__(self, coordinates: [Point]):
        assert len(coordinates) == 2
        super().__init__(coordinates)
        self.points = coordinates

    @staticmethod
    def revert(line):
        return Line(line.points[::-1])

    @staticmethod
    def doubling(line):
        x = (line.points[1].x - line.points[0].x) * 2
        y = (line.points[1].y - line.points[0].y) * 2
        return Line(
            [Point(line.points[0].x - x, line.points[0].y - y), Point(line.points[1].x + x, line.points[1].y + y)])


class Circle(Polygon):
    def __init__(self, x, y, r):
        self.x, self.y, self.r = x, y, r
        self.point = Point(x, y)
        super().__init__(self.point.buffer(r).exterior.coords)
        pass

    def __lt__(self, other):
        return self.point.distance(Point(0, 0)) < other.point.distance(Point(0, 0))

    def equals(self, other):
        return self.x == other.x and self.y == other.y and self.r == other.r

def rotate(line: Line, point_of_rotate: Point, alpha: float = pi / 2):
    pass
    x0 = -sin(alpha) * (line.points[0].y - point_of_rotate.y) + \
         cos(alpha) * (line.points[0].x - point_of_rotate.x) + \
         point_of_rotate.x

    y0 = cos(alpha) * (line.points[0].y - point_of_rotate.y) + \
         sin(alpha) * (line.points[0].x - point_of_rotate.x) + \
         point_of_rotate.y

    x1 = -sin(alpha) * (line.points[1].y - point_of_rotate.y) + \
         cos(alpha) * (line.points[1].x - point_of_rotate.x) + \
         point_of_rotate.x

    y1 = cos(alpha) * (line.points[1].y - point_of_rotate.y) + \
         sin(alpha) * (line.points[1].x - point_of_rotate.x) + \
         point_of_rotate.y

    return Line([Point(x0, y0), Point(x1, y1)])


def almost_equal(one, other, decimal=6):
    return abs(one.x - other.x) < (10 ** -decimal) and abs(one.y - other.y) < (10 ** -decimal)


def tangents_p_c(point: Point, circle: Circle, rotation=1 or -1) -> Line:
    assert not circle.contains(point)
    rotation_angle = rotation * pi / 2
    central_line = Line.doubling(Line([point, circle.point]))
    tangent = rotate(central_line, point, rotation_angle)
    assert not circle.intersects(tangent)  # because it's very strange if so
    while not central_line.almost_equals(tangent, 3):
        rotation_angle /= 2
        middle = rotate(central_line, point, rotation_angle)
        if circle.intersects(middle):
            central_line = middle
        else:
            tangent = middle
    return Line([point, Point(list(circle.intersection(central_line).coords)[0])])


def tangents_c_c(circle1: Circle, circle2: Circle, rotation=(-1, -1)) -> Line:
    assert not (circle2.is_empty or circle1.is_empty)
    assert circle1 is not circle2
    line = Line.doubling(Line([circle1.point, circle2.point]))
    last_points = (Point(float("+inf"), float("+inf")), Point(float("+inf"), float("+inf")))
    for i in range(1000):
        point = Point(circle1.intersection(line).coords[1])
        line = tangents_p_c(point, circle2, rotation[0])
        line = Line.doubling(line)

        point2 = Point(circle2.intersection(line).coords[0])
        line = Line.revert(tangents_p_c(point2, circle1, rotation[1]))
        line = Line.doubling(line)

        if almost_equal(point, last_points[0], 3) and almost_equal(point2, last_points[1], 3):
            break
        last_points = (point, point2)
    return Line(last_points)
