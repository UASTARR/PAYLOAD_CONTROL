"""Code to plot the controller responses."""

import numpy as np
import matplotlib.pyplot as plt
from models.Naive.controller import BangBangController, LinearController, QuadraticController


b_c = BangBangController()
l_c = LinearController(max_rate_of_roll=2.5)
q_c = QuadraticController(max_rate_of_roll=5, delta=2.5)

roll_rates = np.arange(-10, 10, 0.01)
actions = np.zeros((3, len(roll_rates)))

for i, roll_rate in enumerate(roll_rates):
    actions[0][i] = b_c.choose_action(roll_rate)
    if actions[0][i] == 1:
        actions[0][i] = 30
    elif actions[0][i] == 2:   
        actions[0][i] = -30
    actions[1][i] = l_c.choose_action(roll_rate)
    actions[2][i] = q_c.choose_action(roll_rate)

plt.plot(roll_rates, actions[0], label='BangBang')
plt.plot(roll_rates, actions[1], label='Linear')
plt.plot(roll_rates, actions[2], label='Quadratic')
plt.legend()
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.show()
