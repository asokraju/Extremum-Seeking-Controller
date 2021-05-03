import numpy as np
import matplotlib.pyplot as plt


from tools.ESC import ExtremumSeekingController as ESC

def objective(s, s_min=100):
    """
    minimum is reached at s=s_min
    """
    return -0.5 * ((s - s_min) ** 2)
sampling_freq = 2000.
esc = ESC(Omega_h = 100, Omega_l=10., Omega=25., a=2., b=2., PhaseShift=0.,  SamplingTime=1/sampling_freq, IntegratorGain=1., init_value=0.01)


S = []
M = []
s = 1
N = 1000000
for _ in range(N):
    S.append(s)
    m = objective(s)
    M.append(m)
    s = esc.control(m)

plt.plot(np.arange(N),S)
plt.show()

plt.plot(np.arange(N),M)
plt.show()

