# This program visualizes the song from frequency domain
# Source : https://towardsdatascience.com/understanding-audio-data-fourier-transform-fft-spectrogram-and-speech-recognition-a4072d228520 
# This is for generation of the sine wave 
# Source : https://dsp.stackexchange.com/questions/53125/write-a-440-hz-sine-wave-to-wav-file-using-python-and-scipy

# Most of the graphs in this code uses another file to plot. Thus, g_obj is passed(This paramater can be removed) 

import librosa
from librosa import display
import matplotlib.pyplot as plt
import scipy
from scipy.io import wavfile
import numpy as np
import os
import plot_graph as pg


class Plotting:
	def plot_handling(self):
		filepath = os.path.join(os.getcwd(), "songs/first.wav")
		samples, sampling_rate = librosa.load(filepath, sr= None, mono= True,
											  offset = 0.0, duration = None)
		return samples, sampling_rate
	
	# Calculates general average -- no weights considered
	def calc_average(self, x_axis, y_axis):
		maximum = max(y_axis)
		minimum = min(y_axis)
		average = (maximum + minimum)/2

		return average
	
	# TODO: Can weighted average be calculated and what will be the difference
	def weighted_average(self, x_axis, y_axis):
		pass

	# This plot generation is specific to fft and hence cannot be converted to generalised form
	def fft_plot_generation(self, samples, sampling_rate):
		plt.figure()
		librosa.display.waveplot(y=samples,sr=sampling_rate)
		plt.xlabel("Time (seconds)")
		plt.ylabel("Amplitude")
		plt.title("Actual voice data representation")
		plt.show()

	# Implements a low pass filter to understand the effect of this frequencies in voice
	def low_pass_filter(self, x_axis, y_axis, g_obj):
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

		g_obj.set_labels(['Frequency'],['Amplitude'], 'Low pass Filter')
		g_obj.plot_graph([y_select], x_list=[x_select], mode='Final')

	# Implements a high pass filter to understand the effect of high frequencies 
	def high_pass_filter(self, x_axis, y_axis, g_obj):
		x_select = []
		y_select = []

		average = self.calc_average(x_axis, y_axis)
		for i in range(0, len(y_axis)):
			if y_axis[i] >= average:
				x_select.append(x_axis[i])
				y_select.append(y_axis[i])

		print("Selected length", len(x_select), len(y_select))
		print("Actual length", len(x_axis), len(y_axis))

		g_obj.set_labels(['Frequency'],['Amplitude'], 'High pass Filter')
		g_obj.plot_graph([y_select], x_list=[x_select], mode='Final')

	# Implements the effects of removing very high and very low frequencies	
	def band_pass_filter(self, x_axis, y_axis, g_obj):
		pass

	# TODO: Check if the symmentry exist in all Fourier waves. 
	# TODO: Postulate as to why this symmnetry exist and how we can use to our advantage
	def check_symmentry(self, amplitude):
		pass
	

	# The inverse fourier transform has imaginary numbers 
	# Viewing to make sure that the imaginary value is always a zero
	def plot_with_imaginary(self, y):
		t = t = np.arange(len(y))
		plt.plot(t, y.real, 'b-', t, y.imag, 'r--')
		plt.legend(('real', 'imaginary'))
		plt.title("Inverse Fourier transform with imaginary values")
		plt.show()		

	# Checks if the imaginary part is zero and converts it to a list of real numbers
	def convert_to_real(self, y):
		# TODO: Must include assert statement later
		y_real = []
		for value in y:
			y_real.append(value.real)
		return y_real

	# Converts the fourier wave back to original wave 
	# TODO: Play this back and see the changes 	
	def inverse_fft_plot(self, samples, sampling_rate, g_obj):
		y = scipy.fft.ifft(samples)
		#self.plot_with_imaginary(y) 	
		y_real = self.convert_to_real(y)	

		#g_obj.set_labels(['Amplitude'], ['Time in sec'], 'Inverse Fourier to the original wave')
		#g_obj.plot_graph([y], mode= 'Final')

		return y_real 

	# Converts the amplitude of the wave to frequency
	def fft_plot(self, samples, sampling_rate, g_obj):
		n = len(samples)
		T = 1/ sampling_rate
		yf = scipy.fft.fft(samples)
		print("Length after conversion " + str(len(yf)))
		print("Length before conversion " + str(n))
		print("Sampling rate " + str(T))
		xf = np.linspace(0.0, 1.0/(2.0*T), n//2)
		y = 2.0/n * np.abs(yf[:n//2])
		print("Printing length after conversion "+ str(len(y)))

		g_obj.set_labels(['Frequency'],['Amplitude'], 'Fourier Transform Wave')
		g_obj.plot_graph([y], x_list=[xf], mode = 'Final')	
			
		return xf, y, yf

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
	g_obj = pg.Graphs()

	p.generate_sine_wav()

	samples, sampling_rate = p.plot_handling()
	duration_of_sound = len(samples)/ sampling_rate
	print(samples.dtype)

	p.fft_plot_generation(samples, sampling_rate)

	xf, y, yf = p.fft_plot(samples, sampling_rate, g_obj)
	y_inv = p.inverse_fft_plot(yf, sampling_rate, g_obj)
	
	# TODO: This part must be checked with the actual code implemented
	y_np_array = np.array(y_inv, np.float32 	)
	print(y_np_array.dtype)

	# To write to a file 
	wavfile.write('songs/InverseFourier.wav', sampling_rate, samples)
	print(samples[:10])
	print(y_np_array[:10])

	# Calling low pass and high pass filter
	#p.low_pass_filter(xf, y, g_obj)
	#p.high_pass_filter(xf, y, g_obj)


if __name__ == '__main__':
	main()
