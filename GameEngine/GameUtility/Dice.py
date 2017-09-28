import numpy as np


class Dice:
    def __init__(self, min_value=1, max_value=6):
        self.min_value = min_value
        self.max_value = max_value

    def launch(self):
        return np.random.uniform(self.min_value, self.max_value)