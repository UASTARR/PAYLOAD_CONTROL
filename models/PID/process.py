import matplotlib.pyplot as plt
import numpy as np

from drag import Drag

class Process:
    def __init__(self, physics: Drag):
        self.physics = physics
        # There are 4 grid fins that work in pairs, and only one pair at a time
        # is active. One pair is used to increase roll to the left, and the
        # other pair is used to increase roll to the right.
        self.gridfin_left = 0.0
        self.gridfin_right = 0.0

        # Roll is the current rotational speed, in m/s, and is the integral of
        # F = ma over time. We could use torque, or rotational force, and rotational
        # velocity, but it's all linear transformations between them.
        self.roll = 0.0

        # since the effective area of the grid fins reaches a peak at some
        # rotation, there is no point turning the fins past that peak
        self.max = self.physics.drag(0.1*0.1)

    def set_initial_conditions(self, roll):
        self.gridfin_left = 0.0
        self.gridfin_right = 0.0
        self.roll = roll

    def step(self, u):
        """ Process the drive signal to obtain the control signal: y = P(u)
        
        The Plant or process, P, takes a drive signal, u, and produces a
        measurable process variable, y. In our case, the plant is the space
        craft containing the grid fins. The drive force is the result of
        ratating the grid fin to change the drag on the ship.

        Each step applies the force to the current state of the plant and
        determines a new value for the control signal (roll in m/s)
        """
        if u >= 0.0:
            # If force is "positive", it means we want to rotate clock-wise,
            # which is done with the "right-turn" grid fins. Since only one
            # pair is active at a time
            if self.gridfin_left > 0:
                # switch from left turn to right turn
                self.gridfin_left = 0.0
                self.gridfin_right = u
            else:
                # more right turn!
                self.gridfin_right += u

            if self.gridfin_right > self.max:
                    self.gridfin_right = self.max
        else:
            # Negative force - rotate counter-clockwise
            if self.gridfin_right > 0:
                # switch from right turn to left turn
                self.gridfin_right = 0.0
                self.gridfin_left = u
            else:
                # Harder to port!
                self.gridfin_left += u

            if self.gridfin_left > self.max:
                    self.gridfin_left = self.max


        # The fudge factor is converting force (Dyns) to roll (radians/sec)
        fudge = 1.0
        self.roll += fudge * self.physics.drag(u)
        return self.roll
    
if __name__ == "__main__":
    physics = Drag()
    ship = Process(physics)

    t = np.arange(0.0, 100.0, 1.0)
    y = [0.0] * 100

    area = 0.1*0.1/10.0
    f_10percent = physics.drag(area)
    y[0] = ship.step(0)
    y[1] = ship.step(f_10percent)
    for i in range(2, 10):
      y[i] = ship.step(0)

    y[10] = ship.step(-f_10percent)
    for i in range(11, 17):
      y[i] = ship.step(0)
    
    y[17] = ship.step(-f_10percent)
    for i in range(17, 25):
      y[i] = ship.step(0)

    y[25] = ship.step(-f_10percent)
    for i in range(26, 32):
      y[i] = ship.step(0)

    y[32] = ship.step(f_10percent)
    y[33] = ship.step(f_10percent)
    for i in range(34, 40):
      y[i] = ship.step(0)

    y[40] = ship.step(-f_10percent)
    y[41] = ship.step(0)
    y[42] = ship.step(0)
    y[43] = ship.step(-f_10percent)
    for i in range(44, 50):
      y[i] = ship.step(0)

    fig, ax = plt.subplots()

    ax.plot(t, y)

    ax.set(xlabel='time (s)', ylabel='F_roll', title='Roll')

    plt.show()
