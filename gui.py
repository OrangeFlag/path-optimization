import sys, os, pygame, random
from pygame.locals import *

from genetic_algorithms import Path, PathFinder
from input import InputBuilderFromJson

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TEXTCOLOR = (0, 0, 0)
width, height = 800, 800


def td(x):
    return int(x * 400)


class SimpleGui:
    def config(self):
        pass

    def __init__(self):
        self.config()
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Нахождение оптимальных путей в этом жестоком мире')
        self.screen = pygame.display.get_surface()
        background = pygame.Surface(self.screen.get_size()).convert()
        self.screen.fill(WHITE)
        pygame.display.update()

    def draw_path(self, path: Path):
        for j, path_element in enumerate(path.value):
            if path_element.__class__ is Path.StraightWay:
                pygame.draw.line(self.screen, (0, 255, 0),
                                 (300 + td(path_element.line.points[0].x), 300 + td(path_element.line.points[0].y)),
                                 (300 + td(path_element.line.points[1].x), 300 + td(path_element.line.points[1].y)), 3)
                pygame.display.update()

    def draw_circles(self, circles):
        pygame.draw.circle(self.screen, BLUE, (300 + td(0), 300 + td(0)), 3)
        pygame.draw.circle(self.screen, BLUE, (300 + td(1), 300 + td(1)), 3)
        for circle in circles:
            pygame.draw.circle(self.screen, BLUE, (300 + td(circle.x), 300 + td(circle.y)), td(circle.r))
        pygame.display.update()

    def clean_screen(self):
        self.screen.fill(WHITE)

    def start(self):
        while True:
            if self.quit_checker():
                return
            yield ()

    def quit_checker(self):
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                return True
        return False
