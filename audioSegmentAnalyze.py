# Author: Liang Ge
# Audio Strings LLC (c) 2017
# This program analyzes a song segment define from timeBegin to timeEnd, and search for multiple notes match.

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
        				92.498605, 97.998858, 103.82617, 110.000000, 116.54094, 123.47082,			\
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
# Segment information					#
# ------------------------------------- #
timeBegin = 1.35
timeEnd = 1.8
notes = np.array([14])

# ------------------------------------- #
# Set Short-time FFT parameters			#
# ------------------------------------- #
windowSize = 4096*2
fftSize = 4096*2
hopSize = 557
freqObseve = 3000

freqBin = rate / float(fftSize)
print 'FreqBin = ', freqBin, 'Hz'
freqStop = int(math.ceil(freqObseve/freqBin))

windowHamming = 0.54 - 0.46 * np.cos(2*pi/(windowSize-1) * np.arange(windowSize))
window = windowHamming

frameBegin = int(math.floor(rate * timeBegin / hopSize ))
frameEnd = int(math.ceil(rate * timeEnd / hopSize))
print 'frameBegin = ', frameBegin
print 'frameEnd = ', frameEnd

# ------------------------------------- #
# Run algorithm							#
# ------------------------------------- #
peakThreshold = 0.01
errorRatio = 0.03
isNotesMatch = np.ones(len(notes)) * False

for i in range(frameBegin+1, frameEnd-1):
	# Construct the current frame in time domain
	frameStart = i*hopSize
	if (frameStart+windowSize) <= data.size: 
		frame_x = data[frameStart:(frameStart+windowSize)]
	else:
		frame_x = data[frameStart:data.size]
		frame_x = np.append(frame_x, np.zeros(window.size - frame_x.size))
	fft_x = np.append(frame_x * window, np.zeros(fftSize-frame_x.size))
	X = fft(fft_x)
	Xabs = abs(X)
	maxXabs = np.max(Xabs)

	# start searching for notes
	numNotesMatched = 0
	for j in range(freqStop):
		# Find frequency peaks
		if (Xabs[j] > maxXabs * peakThreshold) & (Xabs[j] >= Xabs[j-1]) & (Xabs[j] > Xabs[j+1]):
			freqPeak = j * freqBin
			# Check whether the frequency peak matches the expected notes
			for k in range(len(notes)):
				freqNote = freqBase[notes[k]]
				freqDif1 = abs(freqPeak - freqNote)
				freqDif2 = abs(freqPeak/2 - freqNote)
				if (freqDif1 < freqNote * errorRatio) | (freqDif2 < freqNote * errorRatio):
					if isNotesMatch[k] == False:
						isNotesMatch[k] = True
						numNotesMatched = numNotesMatched + 1
						break
	
	if numNotesMatched == len(notes):
				print '---------------------------------------'
				print 'Yes! Multiples notes have been matched!'
				print '---------------------------------------'
				print 'Time = ', float(i * hopSize) / rate, 's'
				break		

# ------------------------------------- #
# Output								#
# ------------------------------------- #