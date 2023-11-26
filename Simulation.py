import pygame, sys
import numpy as np

from Person import Person, RED, ORANGE, SEAGREEN, GREEN, BACKGROUND, BLUE


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
            person = Person(x, y, self.WIDTH, self.HEIGHT, color=person_color, velocity=velocity, symptomatic=symptomatic)
            self.infected_container.add(person)  # Dodanie do kontenera zakażonych
        else:
            resistant = np.random.choice([True, False])
            if resistant:
                res_color=SEAGREEN
            else:
                res_color=GREEN
            person = Person(x, y, self.WIDTH, self.HEIGHT, color=res_color, velocity=velocity)
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
            guy = Person(
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
            guy = Person(
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
                    # resistant = np.random.choice([True, False])
                    resistant = guy.resistant
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

        pygame.quit()