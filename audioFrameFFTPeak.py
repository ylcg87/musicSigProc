# Author: Liang Ge
# Acoustic Shield, Inc (c) 2017

import scipy
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft, ifft
import math
from math import pi

rate, data = wavfile.read('sounds/string6_hand.wav', 'r')
if data.ndim == 2:
	data = data[:, 0]

windowSize = 1023
fftSize = 4096
hopSize = 250
freqObseve = 6000

frameStart = 150 * hopSize

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

freqBin = rate / float(fftSize)
freqStop = int(math.ceil(freqObseve/freqBin))

# plt.figure(1)
# plt.plot(time_x, frame_x)
# plt.title('Frame frame_x(t)')
# plt.xlabel('Time')

# plt.figure(2)
# plt.plot(freq_x[0:freqStop], Xabs_dB[0:freqStop])
# plt.title('Frame |FFT(x)|')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('dB')

# plt.show()

# find frequency peaks
threshold_dB = 40
eps = 0
freqPeak = np.array([eps])
index = 1
while index < (freqStop-1):
	if Xabs_dB[index] >= threshold_dB:
		if (Xabs_dB[index-1] <= Xabs_dB[index]) & (Xabs_dB[index] >= Xabs_dB[index+1]):
			freqPeak = np.append(freqPeak, Xabs_dB[index])
		else:
			freqPeak = np.append(freqPeak, eps)
	else:
		freqPeak = np.append(freqPeak, eps)
	index = index + 1

freqPeak = np.append(freqPeak, eps)

plt.figure(2)
plt.plot(freq_x[0:freqStop], Xabs_dB[0:freqStop])
# plt.title('Frame |FFT(x)|')
# plt.xlabel('Frequency (Hz)') 
# plt.ylabel('dB')
plt.stem(freq_x[0:freqStop], freqPeak, 'r')
plt.title('Frame |FFT(x)| Peak Value')
plt.xlabel('Frequency (Hz)')
plt.ylabel('dB')

plt.show()