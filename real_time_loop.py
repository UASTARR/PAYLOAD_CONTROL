"""
Code to create a pipeline for real-time control.

The input will be the accelerometer readings, which will be processed to determine the angle of roll and the rate of roll.
The roll data will be passed to the controllers, which will determine the corresponding fin angle/direction.
The fin angle/direction output will be converted into motor actuations and sent to the motors.


There are four controllers:
1. controller_n: NaiveController
2. controller_ns: NaiveSmoothController
3. controller_pid: PID Controller
4. controller_rl: Learned Controller

To run each controller, 
a. uncomment the line that initializes the controller (before the three functions)
b. uncomment the line that calls the controller (in the process_data function)
c. comment the lines corresponding to the other controllers
"""

from collections import deque
import threading
import time
from inference import InferenceAgent
from hardware_api.orientation import Payload
from models.Naive.controller import NaiveSmoothController
from models.PID.controller import Controller
from models.PID.drag import Drag


### queues for data exchange
input_queue = deque(maxlen=2)
output_queue = deque(maxlen=2)

payload = Payload()
controller_n = NaiveController()
# controller_ns = NaiveSmoothController()
# controller_pid = Controller(Drag(), set_point=0.0)
# controller_rl = InferenceAgent(weights_file_name='results/test/linear_deroller_fins_initroll_0.npy')   # might have to change this to a different file


def generate_data():
    prev_time = time.time()
    prev_roll_angle = payload.get_rollangle()
    
    while True:
        curr_roll_angle = payload.get_rollangle()
        curr_time = time.time()
        roll_rate = (curr_roll_angle - prev_roll_angle) / (curr_time - prev_time)
        prev_roll_angle = curr_roll_angle
        prev_time = curr_time

        data = [curr_roll_angle, roll_rate]

        ### add the data to the queue
        input_queue.append(data)
        time.sleep(2)

def process_data():
    while True:
        ### get the *latest* data from the queue
        try:
            data = input_queue.pop()
        except IndexError:      # in case the queue is empty, wait for a bit
            print('Input queue is empty, sleeping for 0.5s...')
            time.sleep(0.5)
            continue
        
        ### process the data
        action = controller_n.choose_action(data[1])        # expects a single element: a float encoding the rate of roll 
        # action = controller_ns.choose_action(data[1])       # expects a single element: a float encoding the rate of roll
        # action = controller_pid.transfer(data[0])           # expects a single element: a float encoding the roll angle
        # action = controller_rl.choose_action([data[1]])     # expects a python list with a single element: a float encoding the rate of roll

        ### add the output to the output queue
        output_queue.append(action)
        time.sleep(2)

def use_output():
    prev_output = 0
    while True:
        ### get the *latest* output from the queue
        try:
            output = output_queue.pop()
        except IndexError:      # in case the output queue is empty, repeat last action
            output = prev_output
        finally:
            prev_output = output

        ### use the output
        # payload.set_gridfin_angle(output, 0)    # for ns and pid controllers
        # payload.set_gridfin_angle(output, 1)    # for ns and pid controllers    # ToDo: have to test if turning both sets in the same direction is correct
        payload.turn_gridfins(output, 0)        # for n and rl controllers
        payload.turn_gridfins(output, 1)        # for n and rl controller             # ToDo: have to test if turning both sets in the same direction is correct
        
        time.sleep(0.01)        # reducing this might result in a lot of actions repeating


### start the threads
threading.Thread(target=generate_data).start()
time.sleep(0.5)
threading.Thread(target=process_data).start()
time.sleep(1)
threading.Thread(target=use_output).start()
