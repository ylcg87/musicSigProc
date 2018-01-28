# Author: Liang Ge
# Audio Strings LLC (c) 2018

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
freqBase = 	np.array([	# Note A0 - B0
    					27.5, 29.135235, 30.867706, \
    					# Note C1 - B1
    					32.703195, 34.647828, 36.708095, 38.890872, 41.203444, 43.653528, \
    					46.249302, 48.999429, 51.913087, 55, 58.27047, 61.735412, \
    					# Note C2 - B2
    					65.406391, 69.295657, 73.416191, 77.781745, 82.406889, 87.307057, \
    					92.498605, 97.998858, 103.82617, 110, 116.54094, 123.47082, \
    					# Note C3 - B3
    					130.812782, 138.591315, 146.832383, 155.563491, 164.813778, 174.614115, \
    					184.997211, 195.997717, 207.652348, 220.000000, 233.081880, 246.941650, \
    					# Note C4 - B4
    					261.625565, 277.182630, 293.664767, 311.126983, 329.627556, 349.228231, \
    					369.994422, 391.995435, 415.304697, 440.000000, 466.163761, 493.883301, \
    					# Note C5 - B5
    					523.251130, 554.365261, 587.329535, 622.253967, 659.255113, 698.456462, \
    					739.988845, 783.990871, 830.609395, 880.000000, 932.327523, 987.766602, \
    					# Note C6 - B6
    					1046.502261, 1108.730523, 1174.659071, 1244.507934, 1318.510227, 1396.912925, \
         				1479.97769, 1567.981743, 1661.21879, 1760, 1864.655046, 1975.533205, \
    					# Note C7 - B7
    					2093.004522, 2217.461047, 2349.318143, 2489.015869, 2637.020455, 2793.825851, \
    					2959.955381, 3135.963487, 3322.43758, 3520, 3729.310092, 3951.06641, \
    					# Note C8
    					4186.009044
        			])

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

# Window for fft
# windowHamming = 0.54 - 0.46 * np.cos(2*pi/(windowSize-1) * np.arange(windowSize))
windowRect = np.ones(windowSize)
window = windowRect

# ------------------------------------- #
# Get current frame data				#
# ------------------------------------- #
frameStart = 431 * hopSize
frame_x = data[frameStart:(frameStart+windowSize)]
time_x = np.arange(frameStart, frameStart+windowSize) * 1.0/rate
# Add zero padding if necessary
fft_x = np.append(frame_x * window, np.zeros(fftSize-windowSize))

# ------------------------------------- #
# Run FFT								#
# ------------------------------------- #
X = fft(fft_x)
Xabs = abs(X)[:fftSize/2]
freqBin = rate / float(fftSize)
freq_x = np.arange(fftSize/2+1) * freqBin
freqStartIndex = int(math.floor(freqMin/freqBin))
freqEndIndex = int(math.ceil(freqMax/freqBin))
# Find the maxFrequency and its magnitude
maxIndex = 0
maxFrequencyMagnitude = Xabs[maxIndex]
for i in range(1, len(Xabs)):
	if Xabs[i] > maxFrequencyMagnitude:
		maxIndex = i
		maxFrequencyMagnitude = Xabs[maxIndex]
maxFrequency = maxIndex * freqBin
print '=> maxFrequency\t\t\t= ', maxFrequency
print '=> maxFrequencyMagnitude\t= ', maxFrequencyMagnitude

# ------------------------------------- #
# Multiple-F0 Detection					#
# ------------------------------------- #
freqErrorRatio = 0.03
magComponentThdRatio = 0.03
H = 10
candidates = np.array([44, 48])
print '=> Multiple F0 = '
for i in range(len(candidates)):
	print '\t', freqBase[candidates[i]]
print '------ Frame Result ------'

for i in range(len(candidates)):
	print 'Analyzing candidate', i
	fc_h_mag = np.array([])
	fc_h_index = np.array([])
	for h in range(1, H+1):
		fc_h = freqBase[candidates[i]] * h
		if fc_h > freqMax:
			fc_h_mag = np.append(f_cc_h_mag, 0)
			fc_h_index = np.append(fc_h_index, 0)
			continue
		indexBottom = int(math.floor((fc_h * (1 - freqErrorRatio))/freqBin))
		indexTop = int(math.ceil((fc_h * (1 + freqErrorRatio))/freqBin))
		# Find the max frequency component
		maxIndex = indexBottom
		for k in range(indexBottom, indexTop+1):
			if Xabs[k] > Xabs[maxIndex]:
				maxIndex = k
		if Xabs[maxIndex] >= maxFrequencyMagnitude*magComponentThdRatio:
			fc_h_mag = np.append(fc_h_mag, Xabs[maxIndex])
			fc_h_index = np.append(fc_h_index, maxIndex)
		else:
			fc_h_mag = np.append(fc_h_mag, 0)
			fc_h_index = np.append(fc_h_index, maxIndex)
	# Check if there exists shared harmonics, update fc_h_mag
	for j in range(i+1, len(candidates)):
		if (candidates[j]-candidates[i]) % 12 == 0:
			print 'Shared harmonics exist'
			# Shared harmonics exists, update fc_h_mag with linear interpolation
			ratio = (candidates[j]-candidates[i]) / 12
			interpolateIndex = ratio
			jump = ratio + 1
			while interpolateIndex < H-2:
				magInterpolate = 0.5 * (fc_h_mag[interpolateIndex-1] + fc_h_mag[interpolateIndex+1])
				if magInterpolate < fc_h_mag[interpolateIndex]:
					fc_h_mag[interpolateIndex] = magInterpolate
				interpolateIndex = interpolateIndex + jump
			break
	print '=> fc_h_mag = \n', fc_h_mag
	print '=> fc_h_index = \n', fc_h_index
	print '=> fc_h_freq = \n', fc_h_index*freqBin
	print '=> energy of all harmonics = ', np.sum(fc_h_mag)
	if (np.sum(fc_h_mag) > maxFrequencyMagnitude*1.3) & (fc_h_mag[0] > 0) &((fc_h_mag[fc_h_mag==0]).size < 4):
		print '**** F0:\t', freqBase[candidates[i]], ' Found'
		# Update Xabs by substracting fc_h_mag
		for index in range(H):
			Xabs[int(fc_h_index[index])] = Xabs[int(fc_h_index[index])] - fc_h_mag[index]
		# Update maxFrequencyMagnitude
		maxIndex = 0
		maxFrequencyMagnitude = Xabs[maxIndex]
		for ii in range(1, len(Xabs)):
			if Xabs[ii] > maxFrequencyMagnitude:
				maxIndex = ii
				maxFrequencyMagnitude = Xabs[maxIndex]
		print 'candidate matched, spectral component removed...'
		print 'new maxFrequencyMagnitude = ', maxFrequencyMagnitude, 'at ', maxIndex*freqBin, '\n'
	else:
		print '**** F0:\t', freqBase[candidates[i]], ' NOT Found\n'
		