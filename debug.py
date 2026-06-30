import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import chirp
#0-15 Hz for 20-30 s
scalingFactor = 1000
t = np.arange(0,30*scalingFactor,0.0001)
# wave = chirp(t, 0, 30,15, method='linear')

wave = chirp(t, 0, 30*scalingFactor,15/(scalingFactor * 2), method='linear', phi=90)
wave = abs(wave)
plt.plot(t, wave)
plt.show()