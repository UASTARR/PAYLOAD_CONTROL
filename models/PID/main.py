import matplotlib.pyplot as plt
import numpy as np

from drag import Drag
from controller import Controller
from process import Process

physics = Drag()
controller = Controller(physics)
ship = Process(physics)

area = 0.1*0.1*3
rotation = physics.drag(area)

ship.set_initial_conditions(rotation)

t = np.arange(0.0, 25.0, 1.0)
y = [0.0] * 25
u = [0.0] * 25

y[0] = ship.step(0.0)
for i in range(1,25):
    u[i] = controller.transfer(y[i-1])
    y[i] = ship.step(u[i])
    
fig, ax = plt.subplots()

ax.plot(t, y, label='roll')
ax.plot(t, u, label='force')

ax.set(xlabel='time (s)', ylabel='F_roll', title='Grid Fin Settings')

plt.show()
