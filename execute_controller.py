"""
Code to run a controller to minimize the roll of the payload.

The input will be the accelerometer readings, which will be processed to determine the rate of roll.
The roll data will be passed to the controller, which will determine the corresponding fin angle.
The fin angle/direction output will be converted into motor actuations and sent to the motors.


We shall be using the linear controller of the five available controllers.
1. controller_bb: BangBangController
2. controller_lin: LinearController
3. controller_hub: HuberController
3. controller_pid: PID Controller
4. controller_rl: Learned Controller
"""

import math
import time
# from hardware_api.orientation import Payload
from execute_controller_test import DummyPayload
from models.Naive.controller import LinearController


# payload = Payload()
payload = DummyPayload(delays=True)
controller = LinearController()
print(f"Ready to run the linear controller...")
started_observing_data = False

with open(f"data_log.tsv", "w") as file:

    while not started_observing_data:
        try:
            prev_roll_angle = payload.get_rollangle()       # ToDo: does this need to be computed again if the next 'try' fails?
            started_observing_data = True
        except Exception as e:
            print(e)
            file.write(f"{time.time()}\twaiting for data...\t0\t0\n")
            time.sleep(1) 
    prev_time = time.time()
    file.write(f"{prev_time}\t{prev_roll_angle}\t0\t0\n")
    print('Started observing data...')

    while True:     # ToDo: use the altitude data to terminate the experiment

        ### compute the required data
        curr_roll_angle = payload.get_rollangle()
        curr_time = time.time()
        roll_rate = (curr_roll_angle - prev_roll_angle) / (curr_time - prev_time)

        ### compute the action
        output = controller.choose_action(roll_rate)       # expects a single element: a float encoding the rate of roll

        ### use the action                          # ToDo: check for +output or -output
        payload.set_gridfin_angle(output, 0)
        payload.set_gridfin_angle(output, 1)        # ToDo: have to test if turning both sets in the same direction is correct
        
        ### log what happened
        file.write(f"{curr_time}\t{curr_roll_angle}\t{roll_rate}\t{output}\n")       # Note: file.write writes in batches
        
        ### reinitialize variables
        prev_roll_angle = curr_roll_angle
        prev_time = curr_time

        time.sleep(0.01)


# As of now, we don't expect to reach this point in the actual experiment
print(f"Experiment complete.")
