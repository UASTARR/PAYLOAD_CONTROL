import time
import board
import adafruit_icm20x

i2c = board.I2C()
icm = adafruit_icm20x.ICM20649(board.I2C())

# 

class Payload:
    def __init__(self):
        self.acceleration = (0, 0, 0)
        self.gyro = (0, 0, 0)
        self.roll_rate = 0
        self.velocity = (0, 0, 33) # m/s
        self.gridfin_orientation = (0, 0) 

    def _update(self, acceleration, gyro):
        self.acceleration = icm.acceleration
        self.roll_rate = icm.gyro[1]
        self.gyro = icm.gyro
        
        
    def _turn_gridfins(self, rel_degrees, grid_fin_pair):
        self.gridfin_orientation[grid_fin_pair] += rel_degrees
        # update the gridfin orientation
        
        
    def _update_orientation(self):
        # madgwick filter here to update the orientation
        
    
        





while True:
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (icm.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f rads/s" % (icm.gyro))
    print("")
    time.sleep(0.5)
