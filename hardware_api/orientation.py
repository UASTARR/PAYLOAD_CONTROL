import time
import board
import adafruit_icm20x
from gpiozero import AngularServo
from time import sleep 
import math 


counterclockwise = -1
still = 0
clockwise = 1

i2c = board.I2C()
icm = adafruit_icm20x.ICM20649(board.I2C())

def rad_to_deg(rad):
    return rad * 180/math.pi

class Payload:
    def __init__(self):
        self.acceleration = (0, 0, 0)
        self.gyro = (0, 0, 0)
        self.roll_rate = 0
        self.velocity = (0, 0, 33) # m/s
        self.gridfin_turning = (still, still)
        self.servo_array = ( # Pin 23 and 24 are pair 1 and Pin 27 and 22 are pair 2
                            AngularServo(23, min_angle=-90, max_angle=90), 
                            AngularServo(24, min_angle=-90, max_angle=90), 
                            AngularServo(27, min_angle=-90, max_angle=90), 
                            AngularServo(22, min_angle=-90, max_angle=90)
                            )
        
    def _update(self, acceleration, gyro):
        self.acceleration = icm.acceleration
        self.roll_rate = icm.gyro[2]
        self.gyro = icm.gyro     

    def _turn_gridfins_full(self, direction, gridfin_pair):
        # gridfin pair is either 0 or 1
        # direction == -1 (left), 1 (right)
        bound = 90 if direction else -90
        self.gridfin_turning[gridfin_pair] = clockwise if direction > 0 else counterclockwise
        for i in range(gridfin_pair*2, gridfin_pair*2 + 1):
            self.servo_array[i].angle = bound

    def _gridfins_origin(self, gridfin_pair):
        self.gridfin_turning[gridfin_pair] = still
        for i in range(gridfin_pair*2, gridfin_pair*2 + 1):
            self.servo_array[i].angle = 0   

    def _get_rollangle(self):
        return rad_to_deg(icm.gyro[2])

    def set_gridfin_angle(self, gridfin_pair, angle):
        for i in range(gridfin_pair*2, gridfin_pair*2 + 1):
            self.servo_array[i].angle = angle       # ToDo: check if these need to be opposite
