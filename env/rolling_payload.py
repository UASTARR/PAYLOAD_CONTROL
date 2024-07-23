"""
This file implements a KSP environment for the de-rolling payload task, 
building on Piotr Kubica's work on using kRPC to control KSP using Python.
"""

import math
import time
import random
import krpc


class RollingPayloadEnv():
    """A simple version of the task with only one action to detumble along the roll axis."""
    def __init__(self, conn, **env_args):
        # self.set_telemetry(conn)
        # self.pre_launch_setup()
        self.conn = conn
        self.quicksave_name = env_args.get("quicksave_name", "1U_2k")

        # self.action_space = spaces.Discrete(9)  # -1, 0, 1 for all axis
        # self.observation_space = spaces.Box(
        #     low=-1, high=1, shape=(2,), dtype=np.float32
        # )

        # self.available_actions = {
        #     "roll": (self.vessel.control.roll, (-1, 0, 1)),
        # }

    def _set_telemetry(self):
        self.vessel = self.conn.space_center.active_vessel
        self.non_rotating_reference_frame = self.vessel.orbit.body.non_rotating_reference_frame

        # Setting up streams for telemetry
        self.ut = self.conn.add_stream(getattr, self.conn.space_center, "ut")
        self.pitch = self.conn.add_stream(getattr, self.vessel.flight(), "pitch")
        self.heading = self.conn.add_stream(getattr, self.vessel.flight(), "heading")
        self.roll = self.conn.add_stream(getattr, self.vessel.flight(), "roll")

    def _pre_launch_setup(self):
        self.vessel.control.sas = False
        self.vessel.control.rcs = False

        self.vessel.parts.with_name('Grid Fin S')[0].modules[1].set_field_bool('Deploy', True)
        self.vessel.parts.with_name('Grid Fin S')[1].modules[1].set_field_bool('Deploy', True)

    def get_state(self):
        state = [
            self.rate_of_roll,
            # self.vessel.flight().surface_altitude
        ]
        return state

    def compute_reward(self):           # maximum reward at zero roll rate
        return -abs(self.rate_of_roll)

    def step(self, action):
        """
        possible continuous actions: yaw[-1:1], pitch[-1:1], roll[-1:1], throttle[0:1],
        other: forward[-1:1], up[-1:1], right[-1:1], wheel_throttle[-1:1], wheel_steering[-1:1],
        available observation
        https://krpc.github.io/krpc/python/api/space-center/control.html
        available states:
        https://krpc.github.io/krpc/python/api/space-center/flight.html
        https://krpc.github.io/krpc/python/api/space-center/orbit.html
        https://krpc.github.io/krpc/python/api/space-center/reference-frame.html
        :param action:
        :return state, reward, termination:
        """
        termination = False

        self._choose_action(action)

        angvel = self.vessel.angular_velocity(self.non_rotating_reference_frame)
        self.rate_of_roll = self.conn.space_center.transform_direction(angvel, self.non_rotating_reference_frame, self.vessel.reference_frame)[1]
        state = self.get_state()
        reward = self.compute_reward()
        # self.conn.ui.message("Reward: " + str(round(reward, 2)), duration=0.2)

        if self.vessel.flight().surface_altitude < 500:
            termination = True
            state = self.reset(seed=0)

        return state, reward, termination

    def _choose_action(self, action):

        ### simple high-level action when using RCS
        # self.vessel.control.roll = (action - 1.0) * 0.4

        ### more complex low-level action to control the gridfins
        if action == -1:
            deploy_angle = -30
        elif action == 1:
            deploy_angle = 30
        else:
            deploy_angle = 0
        
        ### only setting a pair of gridfins for now
        for i in range(2):
            self.vessel.parts.with_name('Grid Fin S')[i].modules[1].set_field_float('Deploy Angle', deploy_angle)

    def reset(self, seed):
        """
        :return: state
        """

        try:
            self.conn.space_center.load(self.quicksave_name)
        except Exception as ex:
            print("Error:", ex)
            exit(f"You have no quick save named '{self.quicksave_name}'. Terminating.")

        # time.sleep(0.1)     # TODO: remove/reduce this for actual experiments

        # game is loaded and we need to reset the telemetry
        self._set_telemetry()
        self._pre_launch_setup()
        self.conn.space_center.physics_warp_factor = 0
        self.rate_of_roll = 0
        self.previous_roll = 0

        state = self.get_state()
        return state


class DummyEnv:
    """A dummy non-KSP environment for simply testing the maintenance of zero roll."""
    def __init__(self, conn, **config) -> None:
        self.rate_of_roll = 5
        self.altitude = 1000

    def get_state(self):
        return [self.rate_of_roll, self.altitude]

    def reset(self, seed=None):
        self.rate_of_roll = 5
        self.altitude = 1000
        return self.get_state()

    def step(self, action):
        torque = (action - 1.0) * 0.5
        self.rate_of_roll += torque
        self.rate_of_roll = max(-15, min(15, self.rate_of_roll))
        reward = -abs(self.rate_of_roll)
        self.altitude -= 10

        if self.altitude <= 100:
            state = self.reset()
            return state, reward, True

        return self.get_state(), reward, False


if __name__ == "__main__":
    conn = krpc.connect(name="TestConnection")
    env = RollingPayloadEnv(conn, quicksave_name="1U_2k")
    state = env.reset(seed=0)
    print(f"Initial state: {state}")
    for i in range(100):
        # action = 1.5)
        action = random.randint(0, 2)
        next_state, reward, termination = env.step(action)
        print(f"{action}\t{reward}\t{termination}\t{next_state}")
        time.sleep(1)
    conn.close()
