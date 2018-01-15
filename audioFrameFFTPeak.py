# Author: Liang Ge
# Audio Strings LLC (c) 2017

import scipy
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft, ifft
import math
from math import pi

folder = 'sounds/piano/testSong/'
file = 'bar1.wav'
rate, data = wavfile.read(folder+file, 'r')

if data.ndim == 2:
	data = data[:, 0]

windowSize = 4096*2
fftSize = 4096*2
hopSize = 557
freqObseve = 3000

frameStart = 170 * hopSize

# frame time domain
frame_x = data[frameStart:(frameStart+windowSize)]

# windowed fft
# windowRect = np.ones(windowSize)
# window = windowRect
windowHamming = 0.54 - 0.46 * np.cos(2*pi/(windowSize-1) * np.arange(windowSize))
window = windowHamming

fft_x = np.append(frame_x * window, np.zeros(fftSize-windowSize))
time_x = np.arange(frameStart, frameStart+windowSize) * 1.0/rate

# frame frequency domain
X = fft(fft_x)
# Xabs_dB = 10.0 * np.log10(abs(X))
Xabs_dB = abs(X)
Xphase = scipy.angle(X) / pi

freqBin = rate / float(fftSize)
freq_x = np.arange(fftSize/2+1) * freqBin
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

plt.figure(1, figsize=(16, 8))
plt.plot(time_x, frame_x)
plt.title('Frame frame_x(t)')
plt.xlabel('Time')

plt.figure(2, figsize=(16, 8))
plt.plot(freq_x[0:freqStop], Xabs_dB[0:freqStop])
# plt.title('Frame |FFT(x)|')
# plt.xlabel('Frequency (Hz)') 
# plt.ylabel('dB')
plt.stem(freq_x[0:freqStop], freqPeak, 'r')
plt.title('Frame |FFT(x)| Peak Value')
plt.xlabel('Frequency (Hz)')
plt.ylabel('dB')

plt.show()