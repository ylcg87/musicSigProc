# Author: Liang Ge
# Audio Strings LLC (c) 2017
# https://en.wikipedia.org/wiki/Fast_Fourier_transform
# https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
# https://en.wikipedia.org/wiki/Window_function

import scipy
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft, ifft
import math
from math import pi

folder = 'sounds/'
file = 'music1.wav'
rate, data = wavfile.read(folder+file, 'r')

if data.ndim == 2:
	data = data[:, 0]

windowSize = 1023
fftSize = 4096
hopSize = 100
freqObseve = 10000

frameStart = 1 * hopSize

# frame time domain
frame_x = data[frameStart:(frameStart+windowSize)]

# windowed fft
windowHamming = 0.54 - 0.46 * np.cos(2*pi/(windowSize-1) * np.arange(windowSize))

window = windowHamming
fft_x = np.append(frame_x * window, np.zeros(fftSize-windowSize))
time_x = np.arange(frameStart, frameStart+windowSize) * 1.0/rate

# frame frequency domain
X = fft(fft_x)
Xabs_dB = 10.0 * np.log10(abs(X))
Xphase = scipy.angle(X) / pi
freq_x = np.arange(fftSize/2+1) * rate / fftSize

plt.figure(1)
plt.plot(time_x, frame_x)
plt.title('Frame frame_x(t)')
plt.xlabel('Time')

freqBin = rate / float(fftSize)
freqStop = int(math.ceil(freqObseve/freqBin))

plt.figure(2)
plt.plot(freq_x[0:freqStop], Xabs_dB[0:freqStop])
plt.title('Frame |FFT(x)|')
plt.xlabel('Frequency')
plt.ylabel('dB')

# plt.figure(3)
# plt.plot(freq_x, Xphase[0:fftSize/2+1])
# plt.title('Frame arg(FFT(x))')
# plt.xlabel('Frequency')
# plt.ylabel('x pi')

plt.show()