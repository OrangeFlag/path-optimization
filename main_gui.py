import os
import sys

from genetic_algorithms import PathFinder
from gui import SimpleGui

from input import InputBuilderFromJson

def get_input_data(file: str):
    print()
    print(file)
    with open(os.path.join(path, file), "r") as f:
        return InputBuilderFromJson.build(f.read())


def start_gui_with_pf(path_finder):
    print("init first generation")
    gui.draw_circles(path_finder.circles)

    for _path in path_finder.generate_path():
        gui.clean_screen()
        gui.draw_circles(path_finder.circles)
        gui.draw_path(_path)
        if gui.quit_checker():
            sys.exit(0)

    print("start_evolution")

    for paths in path_finder.evolute():
        gui.clean_screen()
        gui.draw_circles(path_finder.circles)
        gui.draw_path(paths[0])
        for i in range(5 if 5 <= path_finder.size_generation else path_finder.size_generation):
            print(path_finder.fitness_function(paths[i]), end=" ")
        print()
        if gui.quit_checker():
            sys.exit(0)
    print()
    input("next?")




def start_gui_with_id(input_data, size_generation = 50):
    path_finder = PathFinder(input_data, size_generation=size_generation)
    start_gui_with_pf(path_finder)
    gui.start()



if __name__ == "__main__":
    gui = SimpleGui()
    path = "./input_data/"
    if len(sys.argv) == 1:
        for file in os.listdir(path):
            start_gui_with_id(get_input_data(file))
    else:
        for file in sys.argv[2:]:
            start_gui_with_id(get_input_data(file), int(sys.argv[1]))
