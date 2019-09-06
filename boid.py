import pygame
import random
import math
import numpy as np

from constants import *

"""
TODO: implement spatial separation in update function to let the number of boids increase without killing the
computational speed

TODO: implement boid "view" angles

TODO: implement static obstacles to be avoided
"""

class Flock:
    def __init__(self, win, N):
        self.win = win
        self.boids = [Boid(win) for i in range(N)]

    def draw(self):
        for boid in self.boids:
            boid.draw()

    def update(self):
        for boid in self.boids:
            boid.update(self.boids)


class Boid:
    def __init__(self, win):
        self.win = win
        self.win_height = self.win.get_height()
        self.win_width = self.win.get_width()

        self.pos = np.array((random.random() * self.win_width, random.random() * self.win_height))
        self.center_x = self.pos[0] + BOID_LENGTH / 2
        self.center_y = self.pos[1] + BOID_WIDTH / 2

        self.image = pygame.transform.scale(
            pygame.image.load("boid_sprite.png"), (BOID_LENGTH, BOID_WIDTH))

        self.angle = random.random() * 2* math.pi
        self.v = np.array((BOID_SPEED*math.cos(self.angle), -BOID_SPEED*math.sin(self.angle)))
        self.steering = np.array((0.0, 0.0))

    def update(self, boids):
        """
        Updates the position of the boid using its speed and angle, passing them to a helper function to adjust
        both the (x,y) positions as well as the (center_x, center_y) positions.

        dy has a negative sign because mathematically, "up" is positive y, but in pygame, "up" is negative y.
        :return: None
        """
        # self.steering = np.array((0.0, 0.0))  # commented out to give boids inertia
        self.apply_rules(boids)

        self.apply_force()
        self.change_pos(self.v)

        #### change angle by random amount for now ####
        self.angle += random.uniform(0, .1)

    def apply_rules(self, boids):
        dbar = np.array((0.0, 0.0))  # separate
        vbar = np.array((0.0, 0.0))  # adhere
        posbar = np.array((0.0, 0.0))  # cohere
        total = 0
        for other in boids:
            d = np.linalg.norm(self.pos - other.pos)
            if 0 < d <= BOID_SIGHT:
                dbar += (self.pos - other.pos) / d  # separate with force proportional to distance
                vbar += other.v  # collect the nearby velocities to later average
                posbar = np.average([posbar, other.pos], axis=1, weights=[total / (total + 1), 1 / (total + 1)])
                # average the positions of all the other boids
                total += 1
        if total > 0:
            vbar /= np.linalg.norm(vbar) * BOID_SPEED
            self.steering += dbar + (vbar - self.v) + (posbar - self.pos)

    def apply_force(self):
        new_v = self.v + self.steering / BOID_MASS
        self.angle = math.atan2(-new_v[1], new_v[0])
        self.v[:] = (BOID_SPEED*math.cos(self.angle), -BOID_SPEED*math.sin(self.angle))

    def change_pos(self, v):
        """
        Changes both the (x,y) coordinate and the (center_x, center_y) coordinate in one step. If the new coordinates
        are out of bounds, wrap them around the screen to the other side. Wrapping has a buffer of 2*BOID_LENGTH before
        it kicks in, to allow the sprite to fully exit the window before wrapping.
        :param v: Numpy array
        :return: None
        """
        self.pos += v
        self.center_x += v[0]
        self.center_y += v[1]

        if self.center_x < -2*BOID_LENGTH:
            self.change_pos((self.win_width+BOID_LENGTH, 0))
        if self.center_y < -2*BOID_LENGTH:
            self.change_pos((0, self.win_height + BOID_LENGTH))

        if self.center_x > self.win_width + 2*BOID_LENGTH:
            self.change_pos((-self.win_width-BOID_LENGTH, 0))
        if self.center_y > self.win_height + 2*BOID_LENGTH:
            self.change_pos((0, -self.win_height-BOID_LENGTH))

    def draw(self):
        """
        Rotate the image around its center by self.angle, then blit it to the window.
        :return: None
        """
        img = pygame.transform.rotate(self.image, math.degrees(self.angle))
        img_topleft = img.get_rect(center=(self.center_x, self.center_y)).topleft
        self.win.blit(img, img_topleft)
