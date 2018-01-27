# Author: Liang Ge
# Audio Strings LLC (c) 2017
# https://en.wikipedia.org/wiki/Short-time_Fourier_transform
# http://matplotlib.org/users/image_tutorial.html
# http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.imshow

import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.io import wavfile
from scipy.fftpack import fft, ifft
import math
from math import pi

folder = 'sounds/piano/MuseScore/'
file = 'testMulF0_C4C5.wav'
rate, data = wavfile.read(folder+file, 'r')
# left channel
if data.ndim == 2:
	data = data[:, 0]

# Parameters
windowSize = 4096
fftSize = 4096*2
hopSize = 512
freqObseve = 6000

# windowRect = np.ones(windowSize)
# window = windowRect

# windowTri = np.arange(windowSize/2) * 1.0/(windowSize/2)
# windowTri = np.append(windowTri, 1.0)
# windowTri = np.append(windowTri, 1 - np.arange(1, windowSize/2+1) * 1.0/(windowSize/2))
# window = windowTri

# windowHann = 0.5 * (1 - np.cos(2*pi/(windowSize-1) * np.arange(windowSize)))
# window = windowHann

windowHamming = 0.54 - 0.46 * np.cos(2*pi/(windowSize-1) * np.arange(windowSize))
window = windowHamming

# windowBlackman = 0.42659 - 0.49656*np.cos(2*pi/(windowSize-1) * np.arange(windowSize)) + 0.076849*np.cos(4*pi/(windowSize-1) * np.arange(windowSize))
# window = windowBlackman

# windowBlackmanHarris = 0.35875 - 0.48829*np.cos(2*pi/(windowSize-1) * np.arange(windowSize)) + 0.14128*np.cos(4*pi/(windowSize-1) * np.arange(windowSize)) - 0.01168*np.cos(6*pi/(windowSize-1) * np.arange(windowSize))
# window = windowBlackmanHarris

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

	STFT = np.append(STFT, Xabs_dB[0:fftSize/2+1])

STFT = STFT.reshape(nFrame, fftSize/2+1)

freqBin = rate / float(fftSize)
freqStop = int(math.ceil(freqObseve/freqBin))

plt.figure(1, figsize=(16, 8))
# plt.imshow(STFT, interpolation='nearest', aspect='auto')
plt.imshow(STFT[:, 0:freqStop], interpolation='nearest', aspect='auto')
plt.title(file)
plt.xlabel('Frequency Bin (' + str(freqBin) + ' Hz per bin)')
plt.ylabel('Time Frame')
plt.colorbar()
# plt.savefig(file + ' STFT' + '.png')
plt.show()