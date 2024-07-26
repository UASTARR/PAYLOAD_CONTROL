"""Code to create a pipeline for real-time control.

The input will be the accelerometer readings, which will be processed to determine the rate of roll.
The rate of roll will be passed to the agent, which will determine the corresponding fin direction.
The fin direction output will be converted into motor actuations and sent to the motors.
"""

from collections import deque
import threading
import time
from inference import InferenceAgent
from hardware_api.orientation import Payload
from models.Naive.controller import NaiveSmoothController
from models.PID.controller import Controller
from models.PID.drag import Drag


# queues for data exchange
input_queue = deque(maxlen=2)
output_queue = deque(maxlen=2)
# controller = InferenceAgent(weights_file_name='results/test/linear_deroller_fins_initroll_0.npy')

payload = Payload()
controller_ns = NaiveSmoothController()
# controller_pid = Controller(Drag(), set_point=0.0)


def generate_data():
    prev_time = time.time()
    prev_roll_angle = payload._get_rollangle()
    
    while True:
        curr_roll_angle = payload._get_rollangle()
        curr_time = time.time()
        roll_rate = (curr_roll_angle - prev_roll_angle) / (curr_time - prev_time)
        prev_roll_angle = curr_roll_angle
        prev_time = curr_time

        data = [curr_roll_angle, roll_rate]

        # add the data to the queue
        input_queue.append(data)

def process_data():
    while True:
        # get the *latest* data from the queue
        data = input_queue.pop()
        
        # process the data 
        # print(f'Input: {data}')
        # time.sleep(0.05)        # simulates processing time (which might be the longest part of the loop)
        action = controller_ns.choose_action([data[1]])     # expects a python list with a single element: a float encoding the rate of roll
        # action = controller_pid.transfer(data[0])           # expects a single element: a float encoding the roll angle

        # add the output to the output queue
        output_queue.append(action)

def use_output():
    prev_output = 0
    while True:
        # get the *latest* output from the queue
        try:
            output = output_queue.pop()
        except IndexError:      # in case the output queue is empty, repeat last action
            output = prev_output
        finally:
            prev_output = output

        # use the output
        payload.set_gridfin_angle(0, output)    # ToDo: setting a single pair for now, change as required
        time.sleep(0.01)        # reducing this might result in a lot of actions repeating


def main():

    # start the threads
    threading.Thread(target=generate_data).start()
    threading.Thread(target=process_data).start()
    threading.Thread(target=use_output).start()
