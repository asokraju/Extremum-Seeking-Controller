import numpy as np
import matplotlib.pyplot as plt
import os, sys

# importing local modules
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
print(currentdir, parentdir)
sys.path.append(parentdir)
from tools.ESC import ExtremumSeekingController as ESC


def objective(s, s_min=100):
    """
    minimum is reached at s=s_min
    """
    return -0.5 * ((s - s_min) ** 2)



# Controller
sampling_freq = 2000.
esc = ESC(Omega_h = 100, Omega_l=10., Omega=25., a=2., b=2., PhaseShift=0.,  SamplingTime=1/sampling_freq, IntegratorGain=1., init_value=0.01)


Optimum = []
Optimum_value = []

# initial guess
x = 1

# number of steps
N = 1000000
for _ in range(N):
    Optimum.append(x)
    value = objective(x)
    x = esc.control(value)
    Optimum_value.append(value)

plt.plot(np.arange(N), Optimum)
plt.show()

plt.plot(np.arange(N), Optimum_value)
plt.show()