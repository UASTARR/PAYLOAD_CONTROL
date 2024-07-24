"""Code to create a pipeline for real-time control.

The input will be the accelerometer readings, which will be processed to determine the rate of roll.
The rate of roll will be passed to the agent, which will determine the corresponding fin direction.
The fin direction output will be converted into motor actuations and sent to the motors.
"""

from collections import deque
import threading
import time
from inference import InferenceAgent


# queues for data exchange
input_queue = deque(maxlen=2)
output_queue = deque(maxlen=2)
controller = InferenceAgent(weights_file_name='results/test/linear_deroller_fins_initroll_0.npy')


def generate_data():
    i = 0
    while True:
        # generate random data (ToDo: replace with actual data source)
        data = [i, i+1]
        i+=1 
        # add the data to the queue
        input_queue.append(data)

def process_data():
    while True:
        # get the *latest* data from the queue
        data = input_queue.pop()
        
        # process the data (ToDo: replace with actual processing)
        print(f'Input: {data}')
        time.sleep(0.05)        # simulates processing time (which might be the longest part of the loop)
        action = data[0] % 3 - 1
        # action = controller.choose_action(data)      # the data should be a python list with a single element: a float encoding the rate of roll

        # add the output to the output queue
        output_queue.append(action)

def use_output():
    last_motor_direction = 0
    while True:
        # get the *latest* output from the queue
        try:
            motor_direction = output_queue.pop()
        except IndexError:      # in case the output queue is empty, repeat last action
            motor_direction = last_motor_direction
        finally:
            last_motor_direction = motor_direction

        # use the output (ToDo: send this output to the motors via the Pi)
        print(f'Output: {motor_direction}')
        time.sleep(0.01)        # reducing this might result in a lot of actions repeating


# start the threads
threading.Thread(target=generate_data).start()
threading.Thread(target=process_data).start()
threading.Thread(target=use_output).start()
