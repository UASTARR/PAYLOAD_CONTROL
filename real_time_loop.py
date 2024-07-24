
from collections import deque
import threading
import time

# queues for data exchange
input_queue = deque(maxlen=2)
output_queue = deque(maxlen=2)


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

        # add the output to the output queue
        output_queue.append(data[0] % 3 - 1)

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
