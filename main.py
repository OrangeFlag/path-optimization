import os
import sys

from genetic_algorithms import PathFinder

from input import InputBuilderFromJson


def f_calculations(file: str):
    print()
    print(file)
    with open(os.path.join(path, file), "r") as f:
        input_data = InputBuilderFromJson.build(f.read())
    path_finder = PathFinder(input_data, size_generation=20)
    path_finder.init_first_generation()
    for paths in path_finder.evolute():
        for i in range(5 if 5 <= path_finder.size_generation else path_finder.size_generation):
            print(path_finder.fitness_function(paths[i]), end=" ")
        print()
    print()
    #input("next?")


if __name__ == "__main__":
    path = "./input_data/"
    if len(sys.argv) == 1:
        for file in os.listdir(path):
            f_calculations(file)
    else:
        f_calculations(sys.argv[1])
