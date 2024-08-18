# Code for a naive controller that just asks to roll in the opposite direction of the current roll direction.


def _validate_angle(angle, max_angle):
    if angle > max_angle:
        return max_angle
    elif angle < -max_angle:
        return -max_angle
    return angle


class BangBangController():
    
    def choose_action(self, rate_of_roll):
        if rate_of_roll > 0:        
            return 1                # turn in one direction
        elif rate_of_roll < 0:
            return 2                # turn in the other direction
        return 0                    # neutral position


class LinearController():

    def __init__(self, **kwargs):
        self.max_gridfin_angle_magnitude = kwargs.get('max_gridfin_angle_magnitude', 45)
        self.max_rate_of_roll = kwargs.get('max_rate_of_roll', 5)

    def choose_action(self, rate_of_roll):
        angle = rate_of_roll / self.max_rate_of_roll * self.max_gridfin_angle_magnitude
        return _validate_angle(angle, self.max_gridfin_angle_magnitude)


class QuadraticController():

    def __init__(self, **kwargs):
        self.max_gridfin_angle_magnitude = kwargs.get('max_gridfin_angle_magnitude', 45)
        self.max_rate_of_roll = kwargs.get('max_rate_of_roll', 5)
        self.delta = kwargs.get('delta', 60)

    def _huber_magnitude(self, x):
        x = abs(x)
        if x < self.delta:
            return x**2 / 10
        else:
            return self.delta * (x - self.delta * 0.9)

    def choose_action(self, rate_of_roll):
        angle = self._huber_magnitude(rate_of_roll / self.max_rate_of_roll * self.max_gridfin_angle_magnitude)
        angle = angle if (rate_of_roll > 0) else -angle
        return _validate_angle(angle, self.max_gridfin_angle_magnitude)
