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

rate, data = wavfile.read('sounds/string6_hand.wav', 'r')

if data.ndim == 1:
	# Mono sound
	left_channel = data
	time = np.arange(0, left_channel.size) * 1.0/rate
	plt.figure(1)
	plt.plot(time, left_channel)
	plt.title('Mono Sound')
	plt.show()
elif data.ndim == 2:
	# Stereo sound
	left_channel = data[:, 0]
	right_channel = data[:, 1]
	time = np.arange(0, left_channel.size) * 1.0/rate
	plt.figure(1)
	plt.plot(time, left_channel)
	plt.title('Stereo Left Channel')

	plt.figure(2)
	plt.plot(time, right_channel)
	plt.title('Stereo Right Channel')
	plt.show()