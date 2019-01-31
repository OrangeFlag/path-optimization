import dill as pickle
import unittest
from random import choice

import geometry

from input import InputBuilderFromJson
from genetic_algorithms import Path, PathFinder
from main import f_calculations
from main_gui import get_input_data, start_gui_with_id, start_gui_with_pf


class TestTangents(unittest.TestCase):
    def setUp(self):
        self.point = geometry.Point(2.0, 2.0)
        self.circle = geometry.Circle(0.0, 0.0, 1.0)
        self.circle2 = geometry.Circle(3.0, 3.0, 1.0)

    def test_tangents_p_c(self):
        print()
        print(geometry.tangents_p_c(self.point, self.circle))
        print(geometry.tangents_p_c(self.point, self.circle, rotation=-1))
        self.assertTrue(True)

    def test_tangents_c_c(self):
        def print_(_tuple):
            print(_tuple.points[0].x, _tuple.points[0].y, _tuple.points[1].x, _tuple.points[1].y)

        print()
        print_(geometry.tangents_c_c(self.circle, self.circle2, rotation=(1, 1)))
        print_(geometry.tangents_c_c(self.circle, self.circle2, rotation=(1, -1)))
        print_(geometry.tangents_c_c(self.circle, self.circle2, rotation=(-1, 1)))
        print_(geometry.tangents_c_c(self.circle, self.circle2, rotation=(-1, -1)))
        self.assertTrue(True)


class TestPathFinder(unittest.TestCase):
    def setUp(self):
        with open("./input_data/harder", "r") as f:
            self.input_data = InputBuilderFromJson.build(f.read())

    def test_path(self):
        path_finder = PathFinder(self.input_data, size_generation=10)
        for x in path_finder.generate_path():
            break

    def test_path_finder(self):
        path_finder = PathFinder(self.input_data, size_generation=10)
        path_finder.init_first_generation()

    def test_get_intersected_neigbour(self):
        pass


class TestGA(unittest.TestCase):
    def setUp(self):
        with open("./input_data/harder", "r") as f:
            self.input_data = InputBuilderFromJson.build(f.read())
        self.path_finder = PathFinder(self.input_data, size_generation=20)
        self.path_finder.init_first_generation()

    def test_mutation(self):
        for path in self.path_finder.paths:
            path.mutation()

    def test_crossingover(self):
        self.path_finder.reproduction()
        pass

    def test_selection(self):
        self.path_finder.selection()
        for i in range(self.path_finder.size_generation):
            print(self.path_finder.fitness_function(self.path_finder.paths[i]), end=" ")
        print()


def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def open_object(filename):
    with open(filename, 'rb') as input:
        return pickle.load(input)


class TestWithUI(unittest.TestCase):

    def test_calc_init_generation(self):
        with open("./input_data/harder", "r") as f:
            self.input_data = InputBuilderFromJson.build(f.read())
        self.path_finder = PathFinder(self.input_data, size_generation=50)
        self.path_finder.init_first_generation()
        save_object(self.path_finder, "path_finder_harder_50")

    def test_smth(self):
        self.path_finder = open_object("path_finder_harder_50")
        start_gui_with_pf(self.path_finder)



if __name__ == "__main__":
    unittest.main()
    # TestPathFinder().test_path()
