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
import math

class Plotting:
    def plot_handling(self):
        filepath = os.path.join(os.getcwd(), "songs/first.wav")
        samples, sampling_rate = librosa.load(filepath, sr= None, mono= True,
                                              offset = 0.0, duration = None)
        return samples, sampling_rate
    
    # This plot generation is specific to fft and hence cannot be converted to generalised form
    def fft_plot_generation(self, samples, sampling_rate):
        plt.figure()
        librosa.display.waveplot(y=samples,sr=sampling_rate)
        plt.xlabel("Time (seconds)")
        plt.ylabel("Amplitude")
        plt.title("Actual voice data representation")
        plt.show()

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
        y_real = []
        for value in y:
            y_real.append(value.real)
        return y_real

    # Converts the fourier wave back to original wave 
    # TODO: Play this back and see the changes 	
    def find_inverse_fft(self, samples, sampling_rate):
        return scipy.fft.ifft(samples)		

    # Frequency bins with amplitude and phase
    # TODO: Is there an advantage to convert anngle to degree instead of rad ??
    def get_amp_phase(self, yf):
        return np.abs(yf), np.angle(yf)

    def get_real_imag(self, ampl, phase):
        assert len(ampl) == len(phase), "Error in conversion to amplitude and phase"
        calc_val = []
        for i in range(0, len(ampl)):
            calc_val.append(complex(ampl[i]*math.cos(phase[i]), ampl[i]*math.sin(phase[i])))
        return calc_val

    def get_real_imag_freq(self, ampl, freq, phase):  
        #g_obj = pg.Graphs()
        #g_obj.plot_graph([frequency]) 

        print("Amplitude: ", len(ampl))
        print("Frequency: ", len(freq))
        assert len(ampl) == len(freq), "Error in conversion to amplitude and frequency"
        calc_val = []
        N = (len(ampl) - 1) * 2
        for i in range(0, len(ampl)):
            calc_val.append(complex(ampl[i]*math.cos(2*math.pi*i*freq[i]/N + phase[i]), -ampl[i]*math.sin(2*math.pi*i*freq[i]/N) + phase[i]))
        return calc_val 

    def ampl_freq_back(self, y, N, T):
        ampl, phase = self.get_amp_phase(y)
        frequency = scipy.fft.fftfreq(N, T)[:N//2 + 1]
        value = self.get_real_imag_freq(ampl, frequency, phase)
        return ampl, frequency, value

    def ampl_phase_back(self, y):
        g_obj = pg.Graphs()
        ampl, phase = self.get_amp_phase(y)
        phase_degree = []
        for val in phase:
            phase_degree.append(math.degrees(val))
        g_obj.plot_graph([ampl])
        #g_obj.plot_graph([phase_degree])
        value = self.get_real_imag(ampl, phase)
        return ampl, phase, value

    # Converts the amplitude of the wave to frequency
    def find_fft(self, samples, sampling_rate):
        n = len(samples)
        T = 1/ sampling_rate
        print("Length of the actual song" + str(len(samples)))
        yf = scipy.fft.fft(samples)
        print("Length after Fourier" + str(len(yf)))
        y = yf[:n//2 + 1] 
        # //2 is removed for testing purpose
        xf = np.linspace(0.0, 1.0/(2.0*T), n)
        #y = 2.0/n * np.abs(yf[:n//2])            
        return xf, y, yf

    # This function is used to generate a sine wave with frequency 440 Hz 
    def generate_sine_wav(self):
        sampleRate = 44100
        frequency = 440
        length = 5

        t = np.linspace(0, length, sampleRate * length)  #  Produces a 5 second Audio-File
        y = np.sin(frequency * 2 * np.pi * t)  #  Has frequency of 440Hz

        wavfile.write('songs/Sine.wav', sampleRate, y)

    # The repeated values are conjugated
    def repeat_value(self, y):
        y_new = y
        index = len(y) - 2
        while index > 0:
            y_new = np.append(y_new, np.conjugate(y[index]))
            index -= 1
        return y_new

def check_fft_ifft():
    p = Plotting()
    samples, sampling_rate = p.plot_handling()
    
    # TODO: What is the use of duration of sound and xf?
    #duration_of_sound = len(samples)/ sampling_rate
    #print(samples.dtype, min(samples))
    #p.fft_plot_generation(samples, sampling_rate)
    
    xf, y, y_extra = p.find_fft(samples, sampling_rate)
    yf = p.repeat_value(y)

    return y_extra, yf

# Remember only one g.obj per function
def main():
    g_obj = pg.Graphs()
    p = Plotting()

    #TODO: This section of the code must be changed
    samples, sampling_rate = p.plot_handling()
    y_extra, yf  = check_fft_ifft()
    print(sampling_rate)

    #p.generate_sine_wav()
    #p.plot_with_imaginary(yf)  
    #g_obj.plot_graph([y_extra, yf], divisions= 2)

    y = p.find_inverse_fft(yf, sampling_rate)
    y_inv  = p.convert_to_real(y)
 
    #g_obj.set_labels(['Amplitude'], ['Time in sec'], 'Inverse Fourier to the original wave')
    #g_obj.plot_graph([y_inv], mode= 'Final')
  
    # TODO: This part must be checked with the actual code implemented
    y_np_array = np.array(y_inv, np.float32)

    #g_obj.plot_graph([samples, y_np_array], divisions= 2)
    print(y_np_array.dtype, min(y_np_array))

    # To write to a file 
    wavfile.write('songs/InverseFourier.wav', sampling_rate, samples)

if __name__ == '__main__':
    main()
