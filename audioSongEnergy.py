# Author: Liang Ge
# Audio Strings LLC (c) 2017
# unfinished

import scipy
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft, ifft
import math
from math import pi

# ------------------------------------- #
# File input							#
# ------------------------------------- #
folder = 'sounds/piano/MuseScore/'
file = 'testMulF0_C4C5.wav'
rate, data = wavfile.read(folder+file, 'r')
# Take the left channel
if data.ndim == 2:
	data = data[:, 0]

# ------------------------------------- #
# Set Short-time FFT parameters			#
# ------------------------------------- #
windowSize = 4096
fftSize = 4096*2
hopSize = 512
freqObseve = 3000

# windowHamming = 0.54 - 0.46 * np.cos(2*pi/(windowSize-1) * np.arange(windowSize))
windowRect = np.ones(windowSize)
window = windowRect

nFrame = data.size / hopSize
if (data.size%hopSize) > 0:
	nFrame = nFrame + 1

# ------------------------------------- #
# Run algorithm for frame energy		#
# ------------------------------------- #
runningFrameEnergy = np.array([])
for i in range(nFrame):
	frameStart = i*hopSize
	if (frameStart+windowSize) <= data.size: 
		frame_x = data[frameStart:(frameStart+windowSize)]
	else:
		frame_x = data[frameStart:data.size]
		frame_x = np.append(frame_x, np.zeros(window.size - frame_x.size))
	frameEnergy = 0
	for j in range(windowSize):
		frameEnergy = frameEnergy + abs(frame_x[j])**2
	runningFrameEnergy = np.append(runningFrameEnergy, frameEnergy)

plt.figure(1, figsize=(16, 8))
plt.plot(runningFrameEnergy)

plt.show()