import numpy as np

GREEN = (50, 150, 50)
SEAGREEN = (32,178,170)


class HealthyState:
    def handle_state(self):
        resistant = np.random.choice([True, False])
        return (SEAGREEN if resistant else GREEN), resistant

