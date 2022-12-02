# This code aims to verify over varieds voice signals
# if all the signals are real valued and even
# http://www.openslr.org/12

import glob
import argparse
from tqdm import tqdm
import soundfile as sf
import scipy
from matplotlib import pyplot as plt
import numpy as np
import math

def plot_with_imaginary(y):
        t = t = np.arange(len(y))
        plt.plot(t, y.real, 'b-', t, y.imag, 'r--')
        plt.legend(('real', 'imaginary'))
        plt.title("Inverse Fourier transform with imaginary values")
        plt.show()


def get_amp_phase(yf):
        return np.abs(yf), np.angle(yf)

def determine_fft(samples, sampling_rate):
    N = len(samples)
    T = 1/sampling_rate
    # yf = scipy.fft.fft(samples)[:N//2 + 1]
    y_inter = ampl_freq_back(samples, N, T)
    yf = get_real_imag_freq(y_inter)

    print(yf)
    plot_with_imaginary(yf)

def get_real_imag_freq(ampl, freq, phase):  
    print("Amplitude: ", len(ampl))
    print("Frequency: ", len(freq))
    assert len(ampl) == len(freq), "Error in conversion to amplitude and frequency"
    calc_val = []
    N = (len(ampl) - 1) * 2
    for i in range(0, len(ampl)):
        calc_val.append(complex(ampl[i]*math.cos(2*math.pi*i*freq[i]/N + phase[i]), -ampl[i]*math.sin(2*math.pi*i*freq[i]/N) + phase[i]))
    return calc_val 

def ampl_freq_back(y, N, T):
    ampl, phase = get_amp_phase(y)
    frequency = scipy.fft.fftfreq(N, T)[:N//2 + 1]
    value = get_real_imag_freq(ampl, frequency, phase)
    return ampl, frequency, value

# Read all the songs and return the sample rate and the data of the file
def read_files(args):
    count = 0
    path_to_file = glob.glob(args.path)

    for filepath in tqdm(path_to_file):
        count += 1
        if args.vv:
            print(filepath)
        # Read the data and sample rate of the file
        data, samplerate = sf.read(filepath)
        determine_fft(data, samplerate)

        if count == 10:
            break

        if args.vv:
            print(data)
            print("The value of sample rate is: ", samplerate)

    if args.verbose:
        print(count)

def commandParser():
    parser = argparse.ArgumentParser(description='Fourier Analysis')
    parser.add_argument("--path", help="Path to the type of files that must be read -- give the RE for Glob")
    parser.add_argument("--verbose", action="store_true", help="More details about the results")
    parser.add_argument('-vv', action='store_true', help='Verbose verbose')

    return parser.parse_args()

def main():
    args = commandParser()
    read_files(args)

if __name__ == '__main__':
    main()