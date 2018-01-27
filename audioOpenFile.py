# Author: Liang Ge
# Audio Strings LLC (c) 2017
# Tutorial:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html#scipy.io.wavfile.read
# http://matplotlib.org/users/pyplot_tutorial.html
# https://docs.scipy.org/doc/numpy-dev/user/quickstart.html

import scipy
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

folder = 'sounds/piano/MuseScore/'
file = 'testMulF0_C4C5.wav'
rate, data = wavfile.read(folder+file, 'r')

print 'rate = ', rate

if data.ndim == 1:
	# Mono sound
	left_channel = data
	time = np.arange(0, left_channel.size) * 1.0/rate
	plt.figure(1, figsize=(16, 8))
	plt.plot(time, left_channel)
	plt.title('Mono Sound')
	plt.savefig(file+'.png')
	plt.show()
elif data.ndim == 2:
	# Stereo sound
	left_channel = data[:, 0]
	right_channel = data[:, 1]
	time = np.arange(0, left_channel.size) * 1.0/rate
	plt.figure(1, figsize=(16, 8))
	plt.plot(time, left_channel)
	plt.title(file + ' Stereo Left Channel')
	# plt.savefig(file+'.png')

	plt.figure(2, figsize=(16, 8))
	plt.plot(time, right_channel)
	plt.title(file + 'Stereo Right Channel')
	
	plt.show()