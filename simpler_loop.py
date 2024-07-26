"""
Code to create a pipeline for synchronous (potentially blocking) control.

The input will be the accelerometer readings, which will be processed to determine the angle of roll and the rate of roll.
The roll data will be passed to the controllers, which will determine the corresponding fin angle/direction.
The fin angle/direction output will be converted into motor actuations and sent to the motors.


There are four controllers:
1. controller_n: NaiveController
2. controller_ns: NaiveSmoothController
3. controller_pid: PID Controller
4. controller_rl: Learned Controller

To run each controller, 
a. uncomment the line that initializes the controller
b. uncomment the line that calls the controller (in the process_data function)
c. comment the lines corresponding to the other controllers
d. change the controller_name variable to the corresponding controller (and give a name to the initial conditions!)
"""

import math
import time
from hardware_api.orientation import Payload
from models.Naive.controller import NaiveController
from models.Naive.controller import NaiveSmoothController
from models.PID.controller import Controller
from models.PID.drag import Drag
from inference import InferenceAgent        # ToDo: move this to models/ later.


payload = Payload()
controller_n = NaiveController()
# controller_ns = NaiveSmoothController()
# controller_pid = Controller(Drag(), set_point=0.0)
# controller_rl = InferenceAgent(weights_file_name='results/test/linear_deroller_fins_initroll_0.npy')   # might have to change this to a different file
controller_name = "n"  # or "ns" or "pid" or "rl"       # remember to change this line when changing the controller!
print(f"Starting experiment with controller {controller_name}...")

### set some initial roll
init_roll_direction = 1  # 1 or -1
init_roll_time = 2
start_time = time.time()
while time.time() - start_time < init_roll_time:
    payload.turn_gridfins(init_roll_direction, 0)
    payload.turn_gridfins(init_roll_direction, 1)
    time.sleep(0.1)
name_for_init_roll_conditions = "dir1_2s"
print(f"Initial roll direction {init_roll_direction} for {init_roll_time} seconds (and named {name_for_init_roll_conditions} for logging)...")
print(f"Starting the controller...")

with open(f"{controller_name}_initroll_{name_for_init_roll_conditions}.csv", "w") as file:

    ### now start a controller
    time_to_run = 5
    prev_time = time.time()
    prev_roll_angle = payload.get_rollangle()

    while time.time() - prev_time < time_to_run:
        ### compute the required data
        curr_roll_angle = payload.get_rollangle()
        curr_time = time.time()
        roll_rate = (curr_roll_angle - prev_roll_angle) / (curr_time - prev_time)
        data = [curr_roll_angle, roll_rate]

        ### compute the action
        output = controller_n.choose_action(data[1])        # expects a single element: a float encoding the rate of roll 
        # output = controller_ns.choose_action(data[1])       # expects a single element: a float encoding the rate of roll
        # output = controller_pid.transfer(data[0]*math.pi/180)           # expects a single element: a float encoding the roll angle
        # output = controller_rl.choose_action([data[1]*math.pi/180])     # expects a python list with a single element: a float encoding the rate of roll

        ### use the action                          # ToDo: check for +output or -output
        # payload.set_gridfin_angle(output, 0)    # for ns controller
        # payload.set_gridfin_angle(output, 1)    # for ns controller    # ToDo: have to test if turning both sets in the same direction is correct
        payload.turn_gridfins(output, 0)        # for n, pid, rl controllers            
        payload.turn_gridfins(output, 1)        # for n, pid, rl controller             # ToDo: have to test if turning both sets in the same direction is correct
        
        ### log what happened
        file.write(f"{curr_time - start_time},{curr_roll_angle},{roll_rate},{output}\n")       # writing each step may slow down the loop; consider writing in batches
        
        ### reinitialize variables
        prev_roll_angle = curr_roll_angle
        prev_time = curr_time

        time.sleep(0.01)        # may not be required

print(f"Experiment with controller {controller_name} completed.")
print(f"Resetting the roll to zero...")
payload.set_gridfin_angle(0, 0)
payload.set_gridfin_angle(0, 1)
time.sleep(2)
print("Reset complete. Start a new experiment when ready.")
