
from drag import Drag

class Controller:
    def __init__(self, physics: Drag, set_point=0.0):
        self.physics = physics
        self.K_p = 1.0
        self.set_point = set_point
        self.max_roll = self.physics.drag(0.1*0.1*2)
        
    def transfer(self, y):
        """ The controller takes the error e = setpoint - y as input, applies
        it to the transfer function and produces u, the input to the process.

        The output y and error e are roll values, so we have to convert them
`        through the transfer function to Force.
        """
        e = self.set_point - y
        u = self.K_p * self.physics.area(e)
        return u
 
