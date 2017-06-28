# Author: Liang Ge
# Audio Strings LLC (c) 2017

import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.io import wavfile
from scipy.fftpack import fft, ifft
import math
from math import pi

folder = 'sounds/'
file = 'string1_Pick2.wav'
rate, data = wavfile.read(folder+file, 'r')
# left channel
if data.ndim == 2:
	data = data[:, 0]

# Parameters
windowSize = 1023
fftSize = 4096
hopSize = 100
freqObseve = 6000
threshold_dB = 40
eps = 0

windowHamming = 0.54 - 0.46 * np.cos(2*pi/(windowSize-1) * np.arange(windowSize))
window = windowHamming

freqBin = rate / float(fftSize)
freqStop = int(math.ceil(freqObseve/freqBin))

nFrame = data.size / hopSize
STFT = np.array([])
if (data.size%hopSize) > 0:
	nFrame = nFrame + 1

for i in range(nFrame):
	frameStart = i*hopSize
	if (frameStart+windowSize) <= data.size: 
		frame_x = data[frameStart:(frameStart+windowSize)]
	else:
		frame_x = data[frameStart:data.size]
		frame_x = np.append(frame_x, np.zeros(window.size - frame_x.size))
	fft_x = np.append(frame_x * window, np.zeros(fftSize-frame_x.size))
	X = fft(fft_x)
	Xabs_dB = 10.0 * np.log10(abs(X))
	
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

	STFT = np.append(STFT, freqPeak)

STFT = STFT.reshape(nFrame, freqStop)

plt.figure(1, figsize=(16, 8))
plt.imshow(STFT, interpolation='nearest', aspect='auto')
plt.title(file)
plt.xlabel('Frequency Bin (' + str(freqBin) + ' Hz per bin)')
plt.ylabel('Time Frame')
plt.colorbar()
plt.savefig(file + 'STFT Peak' + '.png')
# plt.show()