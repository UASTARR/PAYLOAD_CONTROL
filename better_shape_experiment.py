import time
from hardware_api.orientation import Payload

def main():
    payload = Payload()

    def measure_time_to_zero_roll(target_degree):
        # Turn fully in the opposite direction for 0.5 seconds
        if target_degree < 0:
            payload._turn_gridfins_full(1, 0)
            payload._turn_gridfins_full(1, 1)
        else:
            payload._turn_gridfins_full(0, 0)
            payload._turn_gridfins_full(0, 1)
        
        time.sleep(0.5)
        
        # Apply the target degree
        payload._turn_gridfins_full(target_degree, 0)
        payload._turn_gridfins_full(target_degree, 1)
        
        # Measure the time to reach zero roll
        start_time = time.time()
        initial_sign = (payload._get_rollangle() > 0)
        
        while True:
            roll_angle = payload._get_rollangle()
            elapsed_time = time.time() - start_time
            if (roll_angle > 0) != initial_sign or elapsed_time >= 5:
                return elapsed_time, roll_angle
            time.sleep(0.1)  # Check every 100 milliseconds

    def reset_to_zero():
        payload._turn_gridfins_full(0, 0)
        payload._turn_gridfins_full(0, 1)
        time.sleep(5)

    with open("roll_angle_data.txt", "w") as file:
        for degree in range(-90, 91):
            time_to_zero, final_roll = measure_time_to_zero_roll(degree)
            file.write(f"{degree}, {time_to_zero:.2f}, {final_roll:.2f}\n")
            print(f"Degree: {degree}, Time to Zero: {time_to_zero:.2f} seconds, Final Roll: {final_roll:.2f}")
            reset_to_zero()

if __name__ == "__main__":
    main()
