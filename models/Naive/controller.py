# Code for a naive controller that just asks to roll in the opposite direction of the current roll direction.

class NaiveController():
    
    def choose_action(self, rate_of_roll):
        if rate_of_roll < 0:        
            return 1                # turn in one direction
        elif rate_of_roll > 0:
            return 2                # turn in the other direction
        return 0                    # neutral position


class NaiveSmoothController():

    def __init__(self):
        self.max_gridfin_angle_magnitude = 30
        self.max_rate_of_roll = 10

    def choose_action(self, rate_of_roll):
        angle = rate_of_roll / self.max_rate_of_roll * self.max_gridfin_angle_magnitude
        return -angle