# This program visualizes the song from frequency domain
# Source : https://towardsdatascience.com/understanding-audio-data-fourier-transform-fft-spectrogram-and-speech-recognition-a4072d228520 
# This is for generation of the sine wave 
# Source : https://dsp.stackexchange.com/questions/53125/write-a-440-hz-sine-wave-to-wav-file-using-python-and-scipy
import librosa
from librosa import display
import matplotlib.pyplot as plt
import scipy
from scipy.io import wavfile
import numpy as np
import os


class Plotting:
	def plot_handling(self):
		filepath = os.path.join(os.getcwd(), "songs/first.wav")
		samples, sampling_rate = librosa.load(filepath, sr= None, mono= True,
											  offset = 0.0, duration = None)
		return samples, sampling_rate
	
	def plot_generation(self, samples, sampling_rate):
		plt.figure()
		librosa.display.waveplot(y=samples,sr=sampling_rate)
		plt.xlabel("Time (seconds) -->")
		plt.ylabel("Amplitude")
		plt.show()


	def plot_graph(self, x_select, y_select, title):
		fig, ax = plt.subplots()
		ax.plot(x_select, y_select)
		plt.grid()
		plt.xlabel("Frequency")
		plt.ylabel("Magnitude")
		plt.title("Plotting with " + title)
		return plt.show()

	def calc_average(self, x_axis, y_axis):
		maximum = max(y_axis)
		minimum = min(y_axis)
		average = (maximum + minimum)/2

		return average

	def low_pass_filter(self, x_axis, y_axis):
		x_select = []
		y_select = []

		average = self.calc_average(x_axis, y_axis)
		print("value of average is ", average)
		for i in range(0, len(y_axis)):
			if y_axis[i] <= average:
				x_select.append(x_axis[i])
				y_select.append(y_axis[i])

		print("Selected length", len(x_select), len(y_select))
		print("Actual length", len(x_axis), len(y_axis))
		self.plot_graph(x_select, y_select, "low pass filter")

	def high_pass_filter(self, x_axis, y_axis):
		x_select = []
		y_select = []

		average = self.calc_average(x_axis, y_axis)
		for i in range(0, len(y_axis)):
			if y_axis[i] >= average:
				x_select.append(x_axis[i])
				y_select.append(y_axis[i])

		print("Selected length", len(x_select), len(y_select))
		print("Actual length", len(x_axis), len(y_axis))
		self.plot_graph(x_select, y_select, "high pass filter")	

	def fft_plot(self, samples, sampling_rate):
		n = len(samples)
		T = 1/ sampling_rate
		yf = scipy.fft(samples)
		print(len(yf))
		print(n)
		print(T)
		xf = np.linspace(0.0, 1.0/(2.0*T), n//2)
		y = 2.0/n * np.abs(yf[:n//2])

		self.plot_graph(xf, y, "Fourier Transform")	

		return xf, y

	# This function is used to generate a sine wave with frequency 440 Hz 
	def generate_sine_wav(self):
		sampleRate = 44100
		frequency = 440
		length = 5

		t = np.linspace(0, length, sampleRate * length)  #  Produces a 5 second Audio-File
		y = np.sin(frequency * 2 * np.pi * t)  #  Has frequency of 440Hz

		wavfile.write('songs/Sine.wav', sampleRate, y)

# TODO: Low pass filter, High pass filter, Curve fitting (Linear and non linear)
# TODO: Fourier of a Fourier and see the graph that it produces
# TODO: Effect of ----- (check in the notes)

def main():
	p = Plotting()
	
	p.generate_sine_wav()

	samples, sampling_rate = p.plot_handling()

	duration_of_sound = len(samples)/ sampling_rate
	p.plot_generation(samples,sampling_rate)
	xf,y = p.fft_plot(samples, sampling_rate)
	p.low_pass_filter(xf, y)
	p.high_pass_filter(xf, y)


if __name__ == '__main__':
	main()
