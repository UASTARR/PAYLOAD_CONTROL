import time
import board
import adafruit_icm20x
from gpiozero import AngularServo
from time import sleep 


counterclockwise = -1
still = 0
clockwise = 1


i2c = board.I2C()
icm = adafruit_icm20x.ICM20649(board.I2C())

 

class Payload:
    def __init__(self):
        self.acceleration = (0, 0, 0)
        self.gyro = (0, 0, 0)
        self.roll_rate = 0
        self.velocity = (0, 0, 33) # m/s
        self.gridfin_turning = (still, still)
        self.servo_array = (
                            AngularServo(23, min_angle=-45, max_angle=45), 
                            AngularServo(24, min_angle=-45, max_angle=45), 
                            AngularServo(27, min_angle=-45, max_angle=45), 
                            AngularServo(22, min_angle=-45, max_angle=45)
                            )
        

    def _update(self, acceleration, gyro):
        self.acceleration = icm.acceleration
        self.roll_rate = icm.gyro[1]
        self.gyro = icm.gyro
        
        
    def _turn_gridfins_rel(self, rel_degrees, gridfin_pair):
        self.gridfin_turning[gridfin_pair] = clockwise if rel_degrees > 0 else counterclockwise
        

    def _turn_gridfins_full(self, direction, gridfin_pair):
        # direction == -1 (left), 1 (right)
        self.gridfin_turning[gridfin_pair] = clockwise if direction > 0 else counterclockwise


    def _gridfins_full_stop(self, gridfin_pair):
        self.gridfin_turning[gridfin_pair] = still
        
        

    def _gridfins_get_rollangle(self):
        return icm.gyro[2]

    def _update_orientation(self):
        # madgwick filter here to update the orientation
        
    
        





while True:
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (icm.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f rads/s" % (icm.gyro))
    print("")
    time.sleep(0.5)
