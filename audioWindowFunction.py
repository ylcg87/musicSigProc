# Author: Liang Ge
# Audio Strings LLC (c) 2017
# https://en.wikipedia.org/wiki/Window_function

import scipy
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft, ifft
import math
from math import pi

# use 500Hz sine function as test function
F = 500
sampRate = 48000
windowSize = 1023
fftSize = 4096
t = np.arange(0, windowSize) * 1.0/sampRate
sine_x = np.sin(2*pi*F*t)

# Window 1 - Rectangular Window
windowRect = np.ones(windowSize)

# Window 2 - Triangular Window
windowTri = np.arange(windowSize/2) * 1.0/(windowSize/2)
windowTri = np.append(windowTri, 1.0)
windowTri = np.append(windowTri, 1 - np.arange(1, windowSize/2+1) * 1.0/(windowSize/2))

# Window 3 - Hann Window
windowHann = 0.5 * (1 - np.cos(2*pi/(windowSize-1) * np.arange(windowSize)))

# Window 4 - Hamming Window
windowHamming = 0.54 - 0.46 * np.cos(2*pi/(windowSize-1) * np.arange(windowSize))

# Window 5 - Blackman Window
windowBlackman = 0.42659 - 0.49656*np.cos(2*pi/(windowSize-1) * np.arange(windowSize)) + 0.076849*np.cos(4*pi/(windowSize-1) * np.arange(windowSize))

# Window 6 - Blackman-Harris Window
windowBlackmanHarris = 0.35875 - 0.48829*np.cos(2*pi/(windowSize-1) * np.arange(windowSize)) + 0.14128*np.cos(4*pi/(windowSize-1) * np.arange(windowSize)) - 0.01168*np.cos(6*pi/(windowSize-1) * np.arange(windowSize))
plt.plot(windowBlackmanHarris)

# view frame fft
fft_x = np.append(sine_x * windowBlackmanHarris, np.zeros(fftSize - windowSize))	# zero padding for fft
X = fft(fft_x)
freq_x = np.arange(fftSize) * sampRate / fftSize