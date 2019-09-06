import pygame

from constants import *
from pygame.locals import QUIT
from boid import Flock


class Game:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.win = pygame.display.set_mode((WIDTH, HEIGHT), 0, 0)
        pygame.display.set_caption("Boid Flocking Simulator")

        self.flock = Flock(self.win, FLOCKSIZE)
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    pygame.quit()

            self.update()
            self.draw()

    def update(self):
        self.flock.update()

    def draw(self):
        self.win.fill((0, 0, 0))
        self.flock.draw()
        pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
