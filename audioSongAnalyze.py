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
# Predefine								#
# ------------------------------------- #
freqBase = 	np.array([	# C2 - B2
						65.406391, 69.295657, 73.416191, 77.781745, 82.406889, 87.307057,	\
        				92.498605, 97.998858, 103.82617, 110, 116.54094, 123.47082,			\
        				# C3 - B3
        				130.812782, 138.591315, 146.832383, 155.563491, 164.813778, 174.614115,	\
        				184.997211, 195.997717, 207.652348, 220.000000, 233.081880, 246.941650,	\
        				# C4 - B4
        				261.625565, 277.182630, 293.664767, 311.126983, 329.627556, 349.228231,	\
        				369.994422, 391.995435, 415.304697, 440.000000, 466.163761, 493.883301,	\
        				# C5 - B5
        				523.251130, 554.365261, 587.329535, 622.253967, 659.255113, 698.456462,	\
        				739.988845, 783.990871, 830.609395, 880.000000, 932.327523, 987.766602	\
        			])

# ------------------------------------- #
# File input							#
# ------------------------------------- #
folder = 'sounds/piano/testSong/'
file = 'bar1.wav'
rate, data = wavfile.read(folder+file, 'r')

if data.ndim == 2:
	data = data[:, 0]

# ------------------------------------- #
# Song information						#
# ------------------------------------- #
# try out with only the 1st bar
Song = list()
subBar1_1 = np.array([14])
subBar1_2 = np.array([21, 31, 33])
subBar1_3 = np.array([14])
subBar1_4 = np.array([21, 31, 33])
Song.append(subBar1_1)
Song.append(subBar1_2)
Song.append(subBar1_3)
Song.append(subBar1_4)

# ------------------------------------- #
# Set Short-time FFT parameters			#
# ------------------------------------- #
windowSize = 4096*2
fftSize = 4096*2
hopSize = 557
freqObseve = 3000

freqBin = rate / float(fftSize)
print 'FreqBin = ', freqBin

windowHamming = 0.54 - 0.46 * np.cos(2*pi/(windowSize-1) * np.arange(windowSize))
window = windowHamming

nFrame = data.size / hopSize
if (data.size%hopSize) > 0:
	nFrame = nFrame + 1

# ------------------------------------- #
# Run algorithm and collect output		#
# ------------------------------------- #
subBarIndex = 0
errorRatio = 0.03
detcMagThreshold = 0.1
isDetc = True

for i in range(nFrame):
	# Calculate frame fft
	frameStart = i*hopSize
	if (frameStart+windowSize) <= data.size: 
		frame_x = data[frameStart:(frameStart+windowSize)]
	else:
		frame_x = data[frameStart:data.size]
		frame_x = np.append(frame_x, np.zeros(window.size - frame_x.size))
	fft_x = np.append(frame_x * window, np.zeros(fftSize-frame_x.size))
	X = fft(fft_x)
	Xabs = abs(X)
	fftData = Xabs

	# Note search
	if isDetc:
		for j in range(1, fftSize/2-1):
			print 'Current j = ', j
			if fftData[j] > detcMagThreshold and fftData[j] >= fftData[j-1] and fftData[j] > fftData[j+1]:
				freqPeak = j * freqBin
				print 'freqPeak = ', freqPeak
				numNote = Song[subBarIndex].size
				for k in range(numNote):
					freqDif = abs(freqPeak-Song[subBarIndex][k])
					freqDif2 = abs(freqPeak/2-Song[subBarIndex][k])
					if freqDif < Song[subBarIndex][k]*errorRatio or freqDif2 < Song[subBarIndex][k]*errorRatio:
						print 'Frame = ', i
						print 'Note Frequency = ', Song[subBarIndex][k]
						k = k + 1

print 'Program Completed...'

# ------------------------------------- #
# Analyze playing performance			#
# ------------------------------------- #