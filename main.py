import pygame, sys
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (64, 64, 64)
BLUE = (0, 100, 255)
GREEN = (50, 150, 50)
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
SEAGREEN = (32,178,170)
BACKGROUND = GREY


class Dot(pygame.sprite.Sprite):

    circle_images = {}

    @staticmethod
    def get_circle_image(color, radius):
        if (color, radius) not in Dot.circle_images:
            image = pygame.Surface([radius * 2, radius * 2], pygame.SRCALPHA)
            pygame.draw.circle(image, color, (radius, radius), radius)
            Dot.circle_images[(color, radius)] = image
        return Dot.circle_images[(color, radius)]

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
        # self.image = pygame.Surface([radius * 2, radius * 2])
        self.image.fill(BACKGROUND)
        # pygame.draw.circle(
        #     self.image, color, (radius, radius), radius
        # )

        self.rect = self.image.get_rect()
        self.pos = np.array([x, y], dtype=np.float64)
        self.vel = np.asarray(velocity, dtype=np.float64)

        self.killswitch_on = False
        self.recovered = False
        self.randomize = randomize

        self.WIDTH = width
        self.HEIGHT = height
        self.symptomatic = symptomatic
        # self.resistant = False
        # if color != RED:
        #     self.resistant = np.random.choice([True, False])
        # if self.resistant:
        #     self.infected = False  # Osoba odporna na zakażenie jest zdrowa
        #     self.symptomatic = False  # Osoba odporna na zakażenie nie ma objawów
        #     color = SEAGREEN
        # else:
        #     self.infected = np.random.choice([True, False])  # Losowe zakażenie
        #     # self.symptomatic = np.random.choice([True, False])  # Losowe wystąpienie
        #     if self.infected == True:
        #         color = RED
        #
        # if color == RED:
        #     self.infected = True
        #     self.symptomatic = np.random.choice([True, False])
        #     if self.symptomatic == False:
        #         color = ORANGE
        self.resistant = np.random.choice([True, False])
        # self.resistant = True
        if self.resistant:
            self.infected = False  # Osoba odporna na zakażenie jest zdrowa
            self.symptomatic = False  # Osoba odporna na zakażenie nie ma objawów
            # pygame.draw.circle(
            #     self.image, SEAGREEN, (radius, radius), radius
            # )
        else:
            self.infected = np.random.choice([True, False])  # Losowe zakażenie
            self.symptomatic = np.random.choice([True, False])  # Losowe wystąpienie
            # if not self.symptomatic and self.infected:
            #     pygame.draw.circle(
            #         self.image, ORANGE, (radius, radius), radius
            #     )
            # else:
            #     pygame.draw.circle(
            #         self.image, color, (radius, radius), radius
            #     )

        pygame.draw.circle(
            self.image, color, (radius, radius), radius
        )

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
        return Dot(
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


class Simulation:
    def __init__(self, width=1000, height=800):
        self.WIDTH = width
        self.HEIGHT = height

        self.susceptible_container = pygame.sprite.Group()
        self.infected_container = pygame.sprite.Group()
        self.recovered_container = pygame.sprite.Group()
        self.all_container = pygame.sprite.Group()
        self.resistant_container = pygame.sprite.Group()

        self.n_susceptible = 20
        self.n_infected = 1
        self.n_quarantined = 0
        self.n_resistant = 0
        self.T = 10000
        self.cycles_to_fate = 20
        self.mortality_rate = 0.0

    def spawn_new_individuals(self):
        side = np.random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            x = np.random.randint(0, self.WIDTH)
            y = 0
        elif side == "bottom":
            x = np.random.randint(0, self.WIDTH)
            y = self.HEIGHT
        elif side == "left":
            x = 0
            y = np.random.randint(0, self.HEIGHT)
        else:
            x = self.WIDTH
            y = np.random.randint(0, self.HEIGHT)

        # Losowanie, czy nowy osobnik będzie zarażony (10% szansa)
        is_infected = np.random.rand() < 0.1

        # Dodanie nowego osobnika do symulacji
        velocity = np.random.rand(2) * 2 - 1
        if is_infected:
            symptomatic = np.random.choice([True, False])
            if symptomatic:
                person_color = RED
            else:
                person_color = ORANGE
            person = Dot(x, y, self.WIDTH, self.HEIGHT, color=person_color, velocity=velocity, symptomatic=symptomatic)
            self.infected_container.add(person)  # Dodanie do kontenera zakażonych
        else:
            resistant = np.random.choice([True, False])
            if resistant:
                res_color=SEAGREEN
            else:
                res_color=GREEN
            person = Dot(x, y, self.WIDTH, self.HEIGHT, color=res_color, velocity=velocity)
            if resistant:
                person.resistant = True
            else:
                person.resistant = False
            if person.resistant:
                self.resistant_container.add(person)
            else:
                self.susceptible_container.add(person)  # Dodanie do kontenera podatnych
        self.all_container.add(person)  # Dodanie do kontenera wszystkich

        # self.total_population += 1  # Zwiększenie całkowitej liczby populacji

    def start(self, randomize=False):

        self.N = (
            self.n_susceptible + self.n_infected + self.n_quarantined
        )

        pygame.init()
        screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])

        for i in range(self.n_susceptible):
            x = np.random.randint(0, self.WIDTH + 1)
            y = np.random.randint(0, self.HEIGHT + 1)
            vel = np.random.rand(2) * 2 - 1
            resistant = np.random.choice([True, False])
            if resistant:
                res_color = SEAGREEN
            else:
                res_color = GREEN
            guy = Dot(
                x,
                y,
                self.WIDTH,
                self.HEIGHT,
                color=res_color,
                velocity=vel,
                randomize=randomize,
            )
            if resistant:
                guy.resistant = True
            else:
                guy.resistant = False
            if guy.resistant:
                self.resistant_container.add(guy)
            else:
                self.susceptible_container.add(guy)
            self.all_container.add(guy)

        for i in range(self.n_infected):
            x = np.random.randint(0, self.WIDTH + 1)
            y = np.random.randint(0, self.HEIGHT + 1)
            vel = np.random.rand(2) * 2 - 1

            symptomatic = np.random.choice([True, False])
            if symptomatic:
                color = RED
            else:
                color = ORANGE
            guy = Dot(
                x,
                y,
                self.WIDTH,
                self.HEIGHT,
                color=color,
                velocity=vel,
                randomize=randomize,
                symptomatic = symptomatic
            )
            self.infected_container.add(guy)
            self.all_container.add(guy)


        clock = pygame.time.Clock()

        for i in range(self.T):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.all_container.update()

            screen.fill(BACKGROUND)

            # New infections
            collision_group = pygame.sprite.groupcollide(
                self.susceptible_container,
                self.infected_container,
                True,
                False,
            )

            for guy in collision_group:
                other_guy = collision_group[guy][0]  # Wybierz pierwszego zderzającego się
                if other_guy.symptomatic:
                    infected = True
                else:
                    infected = np.random.choice([True, False])

                if infected:
                    symptomatic = np.random.choice([True, False])
                    new_guy_color = RED if symptomatic else ORANGE
                else:
                    resistant = np.random.choice([True, False])
                    new_guy_color = SEAGREEN if resistant else GREEN

                new_guy = guy.respawn(new_guy_color, symptomatic if infected else None)
                new_guy.vel *= -1
                new_guy.killswitch(self.cycles_to_fate, self.mortality_rate)

                if infected:
                    self.infected_container.add(new_guy)
                else:
                    self.susceptible_container.add(new_guy)
                self.all_container.add(new_guy)

            # Recoveries
            recovered = [guy for guy in self.infected_container if guy.recovered]
            for guy in recovered:
                new_guy_color = BLUE
                new_guy = guy.respawn(new_guy_color)
                self.recovered_container.add(new_guy)
                self.all_container.add(new_guy)

            self.infected_container.remove(*recovered)
            self.all_container.remove(*recovered)

            self.all_container.draw(screen)

            if i % 5 == 0:
                self.spawn_new_individuals()

            pygame.display.flip()
            clock.tick(25)

        # for i in range(self.T):
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             sys.exit()
        #
        #     self.all_container.update()
        #
        #     screen.fill(BACKGROUND)
        #
        #     # New infections?
        #     collision_group = pygame.sprite.groupcollide(
        #         self.susceptible_container,
        #         self.infected_container,
        #         True,
        #         False,
        #     )
        #
        #     for guy in collision_group:
        #         for other_guy in collision_group:
        #             if other_guy.symptomatic:
        #                 infected = True
        #             else:
        #                 infected = np.random.choice([True, False])
        #             if infected:
        #                 symptomatic = np.random.choice([True, False])
        #                 if symptomatic:
        #                     new_guy_color = RED
        #                 else:
        #                     new_guy_color = ORANGE
        #                 new_guy = guy.respawn(new_guy_color, symptomatic=symptomatic)
        #                 new_guy.vel *= -1
        #                 new_guy.killswitch(
        #                     self.cycles_to_fate, self.mortality_rate
        #                 )
        #                 self.infected_container.add(new_guy)
        #                 self.all_container.add(new_guy)
        #             else:
        #                 resistant = np.random.choice([True, False])
        #                 if resistant:
        #                     res_color = SEAGREEN
        #                 else:
        #                     res_color = GREEN
        #                 new_guy = guy.respawn(res_color)
        #                 if resistant:
        #                     new_guy.resistant = True
        #                 else:
        #                     new_guy.resistant = False
        #                 new_guy.vel *= -1
        #                 self.susceptible_container.add(new_guy)
        #                 self.all_container.add(new_guy)
        #
        #     # Any recoveries?
        #     recovered = []
        #     for guy in self.infected_container:
        #         if guy.recovered:
        #             new_guy = guy.respawn(BLUE)
        #             self.recovered_container.add(new_guy)
        #             self.all_container.add(new_guy)
        #             recovered.append(guy)
        #
        #     if len(recovered) > 0:
        #         self.infected_container.remove(*recovered)
        #         self.all_container.remove(*recovered)
        #
        #     self.all_container.draw(screen)
        #
        #     if i % 5 == 0:
        #         self.spawn_new_individuals()
        #
        #     pygame.display.flip()
        #
        #     clock.tick(25)

        pygame.quit()


if __name__ == "__main__":
    covid = Simulation(1000, 800)
    covid.n_susceptible = 100
    covid.n_quarantined = 0
    covid.n_infected = 5
    covid.cycles_to_fate = np.random.randint(20, 31)*25
    covid.mortality_rate = 0.0
    covid.start(randomize=True)
