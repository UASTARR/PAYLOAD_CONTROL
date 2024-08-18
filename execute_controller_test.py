"""
Code to test execute_controller.py with a dummy payload.
"""

import numpy as np
import time

class DummyPayload:
    def __init__(self, delays=False):
        self.roll_angle = -2     # in radians
        self.delays = delays

    def get_rollangle(self):
        if self.delays:
            time.sleep(np.random.random()*10)
        self.roll_angle += (np.random.random()) * 0.1
        return self.roll_angle

    def set_gridfin_angle(self, angle, fin):
        pass