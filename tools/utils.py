import numpy as np

def sine_generator(SamplingTime:float, sinefreq:float, duration:float):
    """
    return a sampled sine signal of with sampling time:SamplingTime, frequency:sinefreq for a duration:duration
    """
    T = duration
    nsamples = int(SamplingTime * T)
    w = 2. * np.pi * sinefreq
    t_sine = np.linspace(0, T, nsamples, endpoint=False)
    y_sine = np.sin(w * t_sine)
    return t_sine, y_sine