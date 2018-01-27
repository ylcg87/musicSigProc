# Author: Liang Ge
# Audio Strings LLC (c) 2018

import scipy
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft, ifft
import math
from math import pi
import audioFunctions
from audioFunctions import freqBase, frame_multi_F0_match
from audioSongInfo import test1, little_star_1, little_star_2, little_star_3

# ------------------------------------- #
# File input							#
# ------------------------------------- #
folder = 'sounds/piano/MuseScore/'
file = 'little_star_3.wav'
rate, data = wavfile.read(folder+file, 'r')
if data.ndim == 2:
	data = data[:, 0]

# ------------------------------------- #
# Set Short-time FFT parameters			#
# ------------------------------------- #
windowSize = 4096
fftSize = 4096*2
hopSize = 512
freqMin = 20
freqMax = 15000
freqBin = rate / float(fftSize)

# Window for fft
windowHamming = 0.54 - 0.46 * np.cos(2*pi/(windowSize-1) * np.arange(windowSize))
window = windowHamming

# ------------------------------------- #
# Song Information						#
# ------------------------------------- #
Song, numChord, tempo, division = little_star_3()

# ------------------------------------- #
# Multi-F0 Match Algoithm				#
# ------------------------------------- #
chordMatched = np.ones(numChord) * False
timeShiftRatioMinus = 0.02
timeShiftRatioPlus = 0.05
for i in range(numChord):
	print '/-------------- Chord', i, 'to match --------------/'
	# Setup inspect time window
	inspectStartTime = 60/tempo/division * i - 60/tempo/division * timeShiftRatioMinus
	if inspectStartTime < 0:
		inspectStartTime = 0
	inspectEndTime = 60/tempo/division * i + 60/tempo/division * timeShiftRatioPlus
	startIndex = int(math.floor(inspectStartTime*rate/hopSize))
	endIndex = int(math.ceil(inspectEndTime*rate/hopSize))
	
	for j in range(startIndex, endIndex):
		# Get the current frame, and F0 array to be matched
		frameStart = j * hopSize
		print 'frameStart ', frameStart
		frame_x = data[frameStart:(frameStart+windowSize)]
		# Add zero padding if necessary
		fft_x = np.append(frame_x * window, np.zeros(fftSize-windowSize))
		
		# Call multi-F0 match function
		result = frame_multi_F0_match(fft_x, fftSize, rate, freqMin, freqMax, Song[i])
		# Analyze match results
		if result:
			chordMatched[i] = result
			break
# print 'chordMatched = ', chordMatched, '\n'
for i in range(numChord):
	print 'Chord ', i, '\t', chordMatched[i]
print '------------------------------------------------'
print file
print 'Chords Match Result Conclusion:'
print 'Total number of chord:\t', numChord
print 'Match Correct:\t\t', chordMatched[chordMatched==True].size
print 'Match Wrong:\t\t', chordMatched[chordMatched==False].size
print '------------------------------------------------'