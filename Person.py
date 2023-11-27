import pygame, sys
import numpy as np

from Memento import Memento

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (64, 64, 64)
BLUE = (0, 100, 255)
GREEN = (50, 150, 50)
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
SEAGREEN = (32,178,170)
BACKGROUND = GREY


class Person(pygame.sprite.Sprite):

    circle_images = {}

    @staticmethod
    def get_circle_image(color, radius):
        if (color, radius) not in Person.circle_images:
            image = pygame.Surface([radius * 2, radius * 2], pygame.SRCALPHA)
            pygame.draw.circle(image, color, (radius, radius), radius)
            Person.circle_images[(color, radius)] = image
        return Person.circle_images[(color, radius)]

    def __init__(
        self,
        x,
        y,
        width,
        height,
        color=BLACK,
        radius=5,
        velocity=[0, 0],
        randomize=False,
        symptomatic=False
    ):
        super().__init__()
        self.image = self.get_circle_image(color, radius)
        self.image.fill(BACKGROUND)
        self.color = color
        self.rect = self.image.get_rect()
        self.pos = np.array([x, y], dtype=np.float64)
        self.vel = np.asarray(velocity, dtype=np.float64)

        self.killswitch_on = False
        self.recovered = False
        self.randomize = randomize

        self.WIDTH = width
        self.HEIGHT = height
        self.symptomatic = symptomatic
        self.resistant = False

        pygame.draw.circle(
            self.image, color, (radius, radius), radius
        )

    def create_memento(self):
        return Memento(self.color, self.pos)

    def set_memento(self, memento):
        self.color = memento.get_color()
        self.pos = memento.get_position()

    def change_state(self, new_state):
        if new_state == "Susceptible":
            self.state = self.susceptible_state
        elif new_state == "Infected":
            self.state = self.infected_state
        elif new_state == "Recovered":
            self.state = self.recovered_state
        elif new_state == "Resistant":
            self.state = self.resistant_state

    def handle_health(self):
        self.state.handle_state(self)

    def randomize_movement(self, max_speed=2.5, change_direction_prob=0.05):
        if np.random.rand() < change_direction_prob:  # Sprawdzenie szansy na zmianę kierunku
            random_direction = np.random.rand(2) * 2 - 1  # Losowy kierunek
            self.velocity = random_direction * np.random.uniform(0, max_speed)

    def update(self):

        self.pos += self.vel

        x, y = self.pos

        # Sprawdzenie, czy osoba jest poza granicami ekranu, i wtedy zmiana jej położenia
        if x < 0 or x > self.WIDTH or y < 0 or y > self.HEIGHT:
            if np.random.rand() < 0.5:
                self.vel *= -1  # Zawrócenie zmieniając kierunek ruchu
            else:
                self.kill()

        self.rect.x = x
        self.rect.y = y

        self.randomize_movement()
        vel_norm = np.linalg.norm(self.vel)
        if vel_norm > 3:
            self.vel /= vel_norm

        if self.killswitch_on:
            self.cycles_to_fate -= 1

            if self.cycles_to_fate <= 0:
                self.killswitch_on = False
                self.recovered = True

    def respawn(self, color, radius=5, symptomatic=False):
        return Person(
            self.rect.x,
            self.rect.y,
            self.WIDTH,
            self.HEIGHT,
            color=color,
            velocity=self.vel,
            symptomatic=symptomatic
        )

    def killswitch(self, cycles_to_fate=np.random.randint(20, 31)*20, mortality_rate=0.0):
        self.killswitch_on = True
        self.cycles_to_fate = cycles_to_fate
        self.mortality_rate = mortality_rate
