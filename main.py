import numpy as np
from Simulation import Simulation

if __name__ == "__main__":
    disease = Simulation(1000, 800)
    disease.n_susceptible = 100
    disease.n_infected = 5
    disease.cycles_to_fate = np.random.randint(20, 31)*25
    disease.mortality_rate = 0.0
    disease.start(randomize=True)
