import numpy as np

RED = (255, 0, 0)
ORANGE = (255, 140, 0)


class InfectedState:
    def handle_state(self):
        symptomatic = np.random.choice([True, False])
        return (RED if symptomatic else ORANGE), symptomatic