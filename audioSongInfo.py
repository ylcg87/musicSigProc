# Author: Liang Ge
# Audio Strings LLC (c) 2018

import scipy
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft, ifft
import math
from math import pi

def test1():
	Song = np.array([
						[39], #C4 \
						[51], #C5 \
						[39, 51], #C4 C5 \
						[27, 39, 51] #C3 C4 C5\
					])
	numChord = 4
	tempo = 60.0
	division = 1
	
	return Song, numChord, tempo, division

def little_star_1():
	Song = np.array([
						# Measure 1
						[39], #C4 \
						[39], #C4 \
						[46], #G4 \
						[46], #G4 \
						# Measure 2
						[48], #A4 \
						[48], #A4 \
						[46], #G4 \
						[], #X \
						# Measure 3
						[44], #F4 \
						[44], #F4 \
						[43], #E4 \
						[43], #E4 \
						# Measure 4
						[41], #D4 \
						[41], #D4 \
						[39], #C4 \
						[], #X \
						# Measure 5
						[46], #G4 \
						[46], #G4 \
						[44], #F4 \
						[44], #F4 \
						# Measure 6
						[43], #E4 \
						[43], #E4 \
						[41], #D4 \
						[], #X \
						# Measure 7
						[46], #G4 \
						[46], #G4 \
						[44], #F4 \
						[44], #F4 \
						# Measure 8
						[43], #E4 \
						[43], #E4 \
						[41], #D4 \
						[], #X \
						# Measure 9
						[39], #C4 \
						[39], #C4 \
						[46], #G4 \
						[46], #G4 \
						# Measure 10
						[48], #A4 \
						[48], #A4 \
						[46], #G4 \
						[], #X \
						# Measure 11
						[44], #F4 \
						[44], #F4 \
						[43], #E4 \
						[43], #E4 \
						# Measure 12
						[41], #D4 \
						[41], #D4 \
						[39], #C4 \
						[] #X \
					])
	numChord = 48
	tempo = 60.0
	division = 1

	return Song, numChord, tempo, division

def little_star_2():
	Song = np.array([
						# Measure 1
						[39], #C4 \
						[39], #C4 \
						[43, 46], #E4 G4 \
						[43, 46], #E4 G4 \
						# Measure 2
						[39, 48], #C4 A4 \
						[44, 48], #F4 A4 \
						[43, 46], #E4 G4 \
						[], #X \
						# Measure 3
						[38, 44], #B3 F4 \
						[34, 44], #G3 F4 \
						[39, 43], #C4 E4 \
						[39, 43], #C4 E4 \
						# Measure 4
						[38, 41], #B3 D4 \
						[38, 41], #B3 D4 \
						[39], #C4 \
						[], #X \
						# Measure 5
						[43, 46], #E4 G4 \
						[39, 46], #C4 G4 \
						[41, 44], #D4 F4 \
						[38, 44], #B3 F4 \
						# Measure 6
						[34, 43], #G3 E4 \
						[39, 43], #C4 E4 \
						[41], #D4 \
						[], #X \
						# Measure 7
						[38, 46], #B3 G4 \
						[43, 46], #E4 G4 \
						[41, 44], #D4 F4 \
						[38, 44], #B3 F4 \
						# Measure 8
						[34, 43], #G3 E4 \
						[39, 43], #C4 E4 \
						[38, 41], #B3 D4 \
						[], #X \
						# Measure 9
						[39], #C4 \
						[39], #C4 \
						[43, 46], #E4 G4 \
						[39, 46], #C4 G4 \
						[44, 48], #F4 A4 \
						# Measure 10
						[43, 48], #E4 A4 \
						[43, 46], #E4 G4 \
						[], #X \
						# Measure 11
						[41, 44], #D4 F4 \
						[41, 44], #D4 F4 \
						[39, 43], #C4 E4 \
						[43], #E4 \
						# Measure 12
						[34, 41], #G3 D4 \
						[38, 41], #B3 D4 \
						[39], #C4 \
						[] #X \
					])
	numChord = 48
	tempo = 60.0
	division = 1

	return Song, numChord, tempo, division

def little_star_3():
	Song = np.array([
						# Measure 1
						[39], #C4 \
						[], #X \
						[43], #E4 \
						[39], #C4 \
						[43, 46], #E4 G4 \
						[31, 34, 39], #E3 G3 C4 \
						[], #X \
						[39, 43, 46], #C4 E4 G4
						# Measure 2
						[39, 48], #C4 A4 \
						[39, 44, 48], #C4 F4 A4 \
						[44, 48], #*F4 A4 \
						[], #X \
						[43, 46], #E4 G4 \
						[], #X \
						[], #X \
						[], #X \
						# Measure 3
						[38, 44], #B3 F4 \
						[], #X \
						[34, 38, 41], #G3 B3 D4 \
						[34, 44], #G3 F4 \
						[34], #G3 \
						[39, 43], #C4 E4 \
						[39, 43], #C4 E4 \
						[], #X \
						# Measure 4
						[38, 41, 44], #B3 D4 F4 \
						[], #X \
						[32, 38, 41], #F3 B3 D4 \
						[], #X \
						[34, 39], #G3 C4 \
						[], #X \
						[], #X \
						[], #X \
						# Measure 5
						[34, 39, 43, 46], #G3 C4 E4 G4 \
						[34, 39], #G3 C4 \
						[43], #E4 \
						[39, 46], #C4 G4 \
						[41, 44], #D4 F4 \
						[34, 38], #G3 B3 \
						[], #X \
						[34, 38, 41, 44], #G3 B3 D4 F4 \
						# Measure 6
						[34, 39, 43], #G3 C4 E4 \
						[], #X \
						[29, 34, 39, 43], #D3 G3 C4 E4 \
						[], #X \
						[38, 41], #B3 D4 \
						[], #X \
						[], #X \
						[], #X \
						# Measure 7
						[34, 39, 43, 46], #G3 C4 E4 G4 \
						[34, 39], #G3 C4 \
						[43], #E4 \
						[39, 46], #C4 G4 \
						[41, 44], #D4 F4 \
						[34, 38], #G3 B3 \
						[], #X \
						[34, 38, 41, 44], #G3 B3 D4 F4 \
						# Measure 8
						[34, 39, 43], #G3 C4 E4 \
						[], #X \
						[29, 34, 39, 43], #D3 G3 C4 E4 \
						[], #X \
						[38, 41], #B3 D4 \
						[], #X \
						[], #X \
						[], #X \
						# Measure 9
						[39], #C4 \
						[], #X \
						[43], #E4 \
						[39], #C4 \
						[43, 46], #E4 G4 \
						[31, 34, 39], #E3 G3 C4 \
						[], #X \
						[39, 43, 46], #C4 E4 G4
						# Measure 10
						[39, 48], #C4 A4 \
						[39, 44, 48], #C4 F4 A4 \
						[44, 48], #*F4 A4 \
						[], #X \
						[43, 46], #E4 G4 \
						[], #X \
						[], #X \
						[], #X \
						# Measure 11
						[38, 44], #B3 F4 \
						[], #X \
						[34, 38, 41], #G3 B3 D4 \
						[34, 44], #G3 F4 \
						[34], #G3 \
						[39, 43], #C4 E4 \
						[39, 43], #C4 E4 \
						[], #X \
						# Measure 12
						[38, 41, 44], #B3 D4 F4 \
						[], #X \
						[32, 38, 41], #F3 B3 D4 \
						[], #X \
						[34, 39], #G3 C4 \
						[], #X \
						[], #X \
						[], #X \
					])
	numChord = 96
	tempo = 60.0
	division = 2

	return Song, numChord, tempo, division
