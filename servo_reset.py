from time import sleep 
from gpiozero import AngularServo

servo0 = AngularServo(23, min_angle=-90, max_angle=90)
servo1 = AngularServo(24, min_angle=-90, max_angle=90)
servo2 = AngularServo(27, min_angle=-90, max_angle=90)
servo3 = AngularServo(22, min_angle=-90, max_angle=90)

sleep(1)
servo0.angle = 0
servo1.angle = 0
servo2.angle = 0
servo3.angle = 0
sleep(2)
