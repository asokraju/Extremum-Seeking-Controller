import numpy as np
import matplotlib.pyplot as plt
import os, sys

# importing local modules
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)

sys.path.append(parentdir)
from tools.ESC import ExtremumSeekingController as ESC
from Examples.BuckConverter.BuckConverter import Buck_Converter_v0


esc = ESC(Omega_l=10000., Omega_h = 50000., Omega=30000., a=0.01, b=0.01, PhaseShift=0,  SamplingTime=5e-4, IntegratorGain=0.1, init_value=0.04)
env = Buck_Converter_v0()
state = env.reset()
K=0.01
theta = 0.04
udes = env.udes
Theta = []
for i in range(200000):
    controller = env.udes-K*(state[0]-theta*env.Vdes)
    state, r, _,_ = env.step(controller)
    theta = esc.control(10000*r)
    Theta.append(theta)
    if i > 20000 and i<100000:
        if i % 5000==0:
            env.G += 0.001
    # print(r, end ="\r")

path = 'Examples/BuckConverter/'

env.plot(savefig_filename=path + 'input.jpg')
plt.close()

plt.plot(Theta)
plt.savefig(path + 'G.jpg')
plt.close()