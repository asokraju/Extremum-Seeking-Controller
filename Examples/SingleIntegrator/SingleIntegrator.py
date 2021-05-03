import numpy as np
import matplotlib.pyplot as plt
import os, sys

# importing local modules
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)

sys.path.append(parentdir)
from tools.ESC import ExtremumSeekingController as ESC


class ENV():
    """
    """
    def __init__(self, SamplingTime, amin:float =100., freq:float=1000.):
        super(ENV, self).__init__()
        # High pass filter frequency: rad/sec
        self.amin = amin
        self.freq = freq
        self.SamplingTime = SamplingTime
        # simultion time
        self.time = 0.
        self.state = 0
    def compute(self, s):
        self.s_min = self.amin + 1*np.sin(self.freq*2*np.pi*self.time)
        # print(self.time, self.amin, self.s_min, self.freq*2*np.pi*self.time)
        return -0.5 * ((s - self.s_min) ** 2)
    def step(self, u):
        x = self.state
        self.state = u
        self.time += self.SamplingTime
        return x, self.compute(x)


sampling_freq = 2000.
obj = ENV(SamplingTime=1/sampling_freq, amin=10., freq=10.)
esc = ESC(Omega_l=10., Omega_h = 100., Omega=500., a=0.1, b=0.1, PhaseShift=0,  SamplingTime=1/sampling_freq, IntegratorGain=200., init_value=0.01)


S = []
M = []
State = []
s = 1
N = 200000
for _ in range(N):
    S.append(s)
    state, m = obj.step(s)
    M.append(m)
    s = esc.control(m)
    State.append(state)
path = 'Examples/SingleIntegrator/'

plt.plot(np.arange(N),S)
# plt.show()
plt.title('input')
plt.savefig(path + 'input.jpg')
plt.close()


plt.plot(np.arange(N),M)
# plt.show()
plt.title('Optimal_value')
plt.savefig(path + 'Optimal_value.jpg')
plt.close()

plt.plot(np.arange(N),State)
# plt.show()
plt.title('state')
plt.savefig(path + 'state.jpg')
plt.close()