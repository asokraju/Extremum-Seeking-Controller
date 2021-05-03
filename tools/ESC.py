import numpy as np

class ExtremumSeekingController():
    """
    this generates an extremum seeking controller proposed in :
    Krstic, Miroslav, and H-H. Wang. "Stability of extremum seeking feedback for general nonlinear dynamic systems." Automatica 36, no. 4 (2000): 595-601.

    Paper available at: https://www.sciencedirect.com/science/article/abs/pii/S0005109899001831

    This requires four methods:
    1. High pass filter:
        Cutoff frequecy: Omega_h
        Transfer Function = s / (s+Omega_h)
    2. Low pass filter
        Cutoff frequency: Omega_l
        Transfer Function = Omega_l/(s + Omega_l)
    3. Integrator
        Gain: IntegratorGain
        Transfer Function = K/s
    4. Controller that uses the sinusoidal perturbation and all the above three methods to generate the control signal
        Omega: sine frequency in rad/sec
        a, b : gains
        PhaseShift: Phase shift of the sine
    """
    def __init__(self, Omega_h:float, Omega_l:float, Omega:float, a:float, b:float, PhaseShift:float,  SamplingTime:float, IntegratorGain:float, init_value:float=None):
        super(ExtremumSeekingController, self).__init__()
        # High pass filter frequency: rad/sec
        self.Omega_h = Omega_h

        # perturbation sin frequency (rad/sec) and phase shift (rad)
        self.Omega = Omega
        self.a = a
        self.b = b
        self.PhaseShift = PhaseShift


        self.SamplingTime = SamplingTime
        self.IntegratorGain = IntegratorGain

        # high pass filter parameters
        self.high_alpha = 1./(1. + self.Omega_h * self.SamplingTime)
        self.high_u = 1e-3
        self.high_y = 1e-3

        # low pass filter parameters
        self.Omega_l = Omega_l
        if init_value is not None:
            self.low_y = init_value
        # self.low_alpha = np.exp(-self.Omega_l*self.SamplingTime)
        self.low_alpha = 1./(1. + self.Omega_l*self.SamplingTime)
        # integrator parameters
        if init_value is not None:
            self.integrator_s = init_value
        else:
            self.integrator_s = 1e-3

        # simultion time
        self.time = 0.
    def _highpass(self, input: float):
        self.high_y = self.high_alpha * (self.high_y + input - self.high_u)
        self.high_u = input
        return self.high_y
    
    def _lowpass(self, input:float):
        self.low_y = self.low_alpha * (self.low_y) + (1 - self.low_alpha) * input
        return self.low_y

    def _integrator(self, input: float):
        self.integrator_s = self.integrator_s + self.IntegratorGain * self.SamplingTime * input
        return self.integrator_s
    
    def control(self, output:float):
        perturb_m = self.a*np.sin(self.Omega * self.time + self.PhaseShift)
        perturb_a = self.b*np.sin(self.Omega * self.time)

        perturbed_signal =  self._highpass(output) * perturb_m
        low_signal = self._lowpass(perturbed_signal)
        integrated_signal = self._integrator(low_signal)
        theta_hat  = perturb_a + integrated_signal
        self.time += self.SamplingTime
        return theta_hat
