import time
from hardware_api.orientation import Payload

def main():
    t = 10 # seconds delay
    payload = Payload()
    payload._turn_gridfins_full(1, 0)
    payload._turn_gridfins_full(1, 1)
    
    with open("roll_angle_data.txt", "w") as file:
        start_time = time.time()
        for i in range(t):
            roll_angle = payload._get_rollangle()
            elapsed_time = time.time() - start_time
            file.write(f"{elapsed_time:.2f}, {roll_angle:.2f}\n")
            print(roll_angle)
            time.sleep(1)
        
        initial_sign = (roll_angle > 0)
        payload._turn_gridfins_full(0, 0)
        payload._turn_gridfins_full(0, 1)
        
        while True:
            roll_angle = payload._get_rollangle()
            elapsed_time = time.time() - start_time
            file.write(f"{elapsed_time:.2f}, {roll_angle:.2f}\n")
            print(roll_angle)
            if (roll_angle > 0) != initial_sign:
                break
            time.sleep(1)
    
    

if __name__ == "__main__":
    main()
