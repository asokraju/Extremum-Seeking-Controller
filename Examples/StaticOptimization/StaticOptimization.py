import numpy as np
import matplotlib.pyplot as plt
import os, sys

# importing local modules
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)

sys.path.append(parentdir)
from tools.ESC import ExtremumSeekingController as ESC


class Objective():
    """
    Optimizztion problem with varying optimal point.
    """
    def __init__(self,SamplingTime, amin:float =100., freq:float=1000.):
        super(Objective, self).__init__()
        # High pass filter frequency: rad/sec
        self.amin = amin
        self.freq = freq
        self.SamplingTime = SamplingTime
        # simultion time
        self.time = 0.
    def compute(self, s):
        self.s_min = self.amin + 100 * np.sin(self.freq*2*np.pi*self.time)
        self.time += self.SamplingTime
        return -0.5 * ((s - self.s_min) ** 2)



sampling_freq = 2000.
objective = Objective(SamplingTime=1/sampling_freq, amin=10., freq=1000.)
esc = ESC(Omega_l=100., Omega_h = 100., Omega=500., a=0.1, b=0.1, PhaseShift=0,  SamplingTime=1/sampling_freq, IntegratorGain=500., init_value=0.01)



# # Controller
# sampling_freq = 2000.
# esc = ESC(Omega_h = 100, Omega_l=10., Omega=25., a=2., b=2., PhaseShift=0.,  SamplingTime=1/sampling_freq, IntegratorGain=1., init_value=0.01)


Optimum = []
Optimum_value = []

# initial guess
x = 1

# number of steps
N = 40000
for _ in range(N):
    Optimum.append(x)
    value = objective.compute(x)
    x = esc.control(value)
    Optimum_value.append(value)

path = 'Examples/StaticOptimization/'

plt.plot(np.arange(N), Optimum)
# plt.show()
plt.title('optimim')
plt.savefig(path + 'optimim.jpg')
plt.close()

plt.plot(np.arange(N), Optimum_value)
# plt.show()
plt.title('Optimum_value')

plt.savefig(path + 'Optimum_value.jpg')
plt.close()