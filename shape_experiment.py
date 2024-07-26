import time
from hardware_api.orientation import Payload

def main():
    t = 1 # seconds delay
    payload = Payload()
    payload.servo_array[0].angle = -90
    payload.servo_array[1].angle = -90
    payload.servo_array[2].angle = -90
    payload.servo_array[3].angle = -90
    
    with open("roll_angle_data_misc.txt", "w") as file:
        start_time = time.time()
        for i in range(t):
            roll_angle = payload.get_rollangle()
            elapsed_time = time.time() - start_time
            file.write(f"{elapsed_time:.2f}, {roll_angle:.2f}\n")
            print(roll_angle)
            time.sleep(1)
        
        initial_sign = (roll_angle > 0)
        payload.servo_array[0].angle = 90
        payload.servo_array[1].angle = 90
        payload.servo_array[2].angle = 90
        payload.servo_array[3].angle = 90        
        
        while True:
            roll_angle = payload.get_rollangle()
            elapsed_time = time.time() - start_time
            file.write(f"{elapsed_time:.2f}, {roll_angle:.2f}\n")
            print(roll_angle)
            if (roll_angle > 0) != initial_sign:
                break
            time.sleep(1)

        payload.servo_array[0].angle = 0
        payload.servo_array[1].angle = 0
        payload.servo_array[2].angle = 0
        payload.servo_array[3].angle = 0
    
    

if __name__ == "__main__":
    main()
