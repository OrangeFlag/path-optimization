from enum import IntEnum
from random import choice, randrange, random

from shapely.geometry import Point, LineString

from geometry import Circle, Line, tangents_c_c


class Rotation(IntEnum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = -1


def almost_equal(one, other, decimal=3):
    return abs(one - other) < (10 ** -decimal)


class Path:
    class CurveWay:
        def __init__(self, circle: Circle, rotation_choice=None):
            if rotation_choice is None:
                rotation_choice = [Rotation.CLOCKWISE, Rotation.COUNTERCLOCKWISE]
            self.circle = circle
            self.rotation = choice(rotation_choice)
            self.curve: LineString = LineString()

        @staticmethod
        def build(circles, path1, path2, without=None):
            if without is None:
                without = []
            assert path1[-1] is path2[0]
            assert path1[-1].__class__ == Path.CurveWay

            curve_way = path1[-1]
            circle: Circle = curve_way.circle
            start_point: Point = path1[-2].line.points[1]
            i_closest_to_start_point = None
            distance_to_start_point = float("+inf")
            end_point: Point = path2[1].line.points[0]
            i_closest_to_end_point = None
            distance_to_end_point = float("+inf")

            curve = list(map(lambda point: Point(point), circle.exterior.coords[:-1]))
            for i, point in enumerate(curve):
                distance = point.distance(start_point)
                if distance < distance_to_start_point:
                    i_closest_to_start_point = i
                    distance_to_start_point = distance

                distance = point.distance(end_point)
                if distance < distance_to_end_point:
                    i_closest_to_end_point = i
                    distance_to_end_point = distance

            if i_closest_to_end_point != i_closest_to_start_point:
                if i_closest_to_start_point < i_closest_to_end_point:
                    curve_way.curve = LineString(
                        [start_point] + curve[i_closest_to_start_point: i_closest_to_end_point + 1] + [end_point])
                else:
                    curve_way.curve = LineString(
                        [start_point] + curve[i_closest_to_start_point:] + curve[:i_closest_to_end_point + 1] + [
                            end_point])
            else:
                curve_way.curve = LineString(
                    [start_point] + curve[i_closest_to_start_point + 1:] + curve[:i_closest_to_end_point] + [
                        end_point])

            # TODO Нужно чекать, что мы можем обойти круг, если не можем то строить обходной маршрут,
            #  если не можем слать error ( например не можем, если уперлись в стену)
            return path1[:-1] + [curve_way] + path2[1:]

        def length(self):
            return self.curve.length

    class StraightWay:
        def __init__(self, line: Line):
            self.line = line

        @staticmethod
        def build(circles, start_curve_way, end_curve_way, without=None):
            if without is None:
                without = [start_curve_way.circle, end_curve_way.circle]
            else:
                without.append(start_curve_way.circle)
                without.append(end_curve_way.circle)

            def rotation_to_tangent_rotation(start_rotation, end_rotation):
                if (start_rotation, end_rotation) == (1, 1) or (start_rotation, end_rotation) == (-1, -1):
                    return -start_rotation, end_rotation
                elif (start_rotation, end_rotation) == (1, -1) or (start_rotation, end_rotation) == (-1, 1):
                    return start_rotation, -end_rotation

            line = tangents_c_c(start_curve_way.circle, end_curve_way.circle,
                                rotation_to_tangent_rotation(start_curve_way.rotation, end_curve_way.rotation))
            crossed_circle = Path.StraightWay.get_intersected_neigbour(circles, line.points[0],
                                                                       line.points[1], without=without)

            if crossed_circle:
                crossed_curve_way = Path.CurveWay(crossed_circle)
                path1 = Path.StraightWay.build(circles, start_curve_way, crossed_curve_way, without=without)
                path2 = Path.StraightWay.build(circles, crossed_curve_way, end_curve_way, without=without)
                return Path.CurveWay.build(circles, path1, path2, without=without)
            else:
                return [start_curve_way, Path.StraightWay(line), end_curve_way]

        @staticmethod
        def build_through_circle(circles, start_curve_way, end_curve_way, through_circle, without=None):
            through_way = Path.CurveWay(through_circle)
            if not without:
                without = []
            return Path.CurveWay.build(circles,
                                       Path.StraightWay.build(circles, start_curve_way, through_way, without),
                                       Path.StraightWay.build(circles, through_way, end_curve_way, without))

        @staticmethod
        def get_intersected_neigbour(circles: [Circle], start_point: Point, end_point: Point, without=None):
            if without is None:
                without = []
            line = Line([start_point, end_point])
            _min = float('+inf')
            neigbour = None
            for circle in circles:
                if circle in without:
                    continue
                intersection = line.intersection(circle)
                if not intersection.is_empty:
                    minimal = Point(min(list(intersection.coords), key=lambda pair: pair[0] ** 2 + pair[1] ** 2))
                    distance = (start_point.x - minimal.x) ** 2 + (start_point.y - minimal.y) ** 2
                    if distance < _min:
                        _min = distance
                        neigbour = circle
            return neigbour

        def length(self):
            return self.line.length

    def __init__(self, circles=None):
        self.circles = circles
        if circles:
            self.value = self.StraightWay.build(circles, Path.CurveWay(Circle(0.0, 0.0, 1e-10)),
                                                Path.CurveWay(Circle(1.0, 1.0, 1e-10)))
        else:
            self.value = None

    def crossingover(self, other):
        if self is other:
            return None
        try:
            gap = randrange(2, min(len(self.value), len(other.value)) - 2, 2)
        except(ValueError):
            return None
        if self.value[gap].circle.equals(other.value[gap + 2].circle):
            return None

        child = Path()
        child.circles = self.circles
        child.value = self.value[:gap] + Path.StraightWay.build(self.circles, self.value[gap],
                                                                other.value[gap + 2]) + other.value[gap + 3:]
        return child

    def mutation(self):
        try:
            point = randrange(2, len(self.value) - 1, 2)
        except(ValueError):
            return
        circle = choice(self.circles)
        if circle.equals(self.value[point + 2].circle) or circle.equals(self.value[point - 2].circle):
            return
        self.value = self.value[:point - 2] + Path.StraightWay.build_through_circle(self.circles, self.value[point - 2],
                                                                                    self.value[point + 2],
                                                                                    through_circle=circle) + self.value[
                                                                                                             point + 3:]
        pass


class PathFinder:
    def __init__(self, input_data, size_generation=50, mutation_possibility=0.2, fitness_function=None):
        def default_fitness_function(path: Path):
            max_line = 0
            accum_curve = 0
            for element in path.value:
                length = element.length()
                if element.__class__ is Path.StraightWay:
                    if max_line <= length:
                        max_line = length
                else:
                    accum_curve += length
            return accum_curve / max_line

        self.name = input_data[0]
        self.circles = input_data[1]
        self.dt = input_data[2]
        self.Fmax = input_data[3]

        self.paths = []
        self.size_generation = size_generation
        self.mutation_possibility = mutation_possibility
        if not fitness_function:
            self.fitness_function = default_fitness_function

    def init_first_generation(self):
        for i in range(self.size_generation):
            self.paths.append(Path(self.circles))

    def generate_path(self):
        for i in range(self.size_generation):
            path = Path(self.circles)
            self.paths.append(Path(self.circles))
            yield path

    def reproduction(self):
        childs = []
        for i in range(len(self.paths)):
            child = choice(self.paths).crossingover(choice(self.paths))
            if child:
                childs.append(child)
        self.paths.extend(childs)

    def mutation(self):
        for path in self.paths:
            if random() < self.mutation_possibility:
                path.mutation()

    def selection(self):
        self.paths = sorted(self.paths, key=self.fitness_function)[:self.size_generation]

    def evolute(self, n_steps=1000):
        if not self.paths:
            return
        min_fitness = float("+inf")
        count_min_fitness = 0
        for i in range(n_steps):

            self.reproduction()
            self.mutation()
            self.selection()

            yield self.paths

            best_fitness_in_step = self.fitness_function(self.paths[0])
            if almost_equal(best_fitness_in_step, min_fitness):
                count_min_fitness += 1
            else:
                count_min_fitness = 0

            if min_fitness > best_fitness_in_step:
                min_fitness = best_fitness_in_step

            if count_min_fitness == 10:
                break

            last_fitness = self.fitness_function(self.paths[0])

# TODO откалибровать without, кажется он виновен в перечесении с окружностью, сделать нормальные функцию поиска соседей
