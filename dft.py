# Creating Fourier weights
import torch
import librosa
from matplotlib import pyplot as plt
import time

def get_song():
    filepath = './songs/first.wav'
    samples, sampling_rate = librosa.load(filepath,sr= None, mono= True,
                                            offset = 0.0, duration = None)
    return samples, sampling_rate

# Creates the Fourier weights for the given samples
def create_fourier_weights(samples, check_sample_size = 10):
    print("The shape of the samples is: ", samples.shape)
    sample_subset = samples[:check_sample_size]
    # n_val goes vertically, k_val goes horizontally
    k_val, n_val = torch.meshgrid(torch.arange(check_sample_size), torch.arange(check_sample_size))
    theta = 2 * torch.pi * k_val * n_val / check_sample_size
    cos_theta = torch.cos(theta)
    sin_theta = - torch.sin(theta)
    fourier_matrix = torch.stack([cos_theta, sin_theta], dim = -1)
    return fourier_matrix

# Computes the fourier transform
def compute_fourier_transform(samples, fourier_matrix, check_sample_size = 10):
    output = torch.matmul(samples[:check_sample_size], fourier_matrix)
    return output

# Computes the inverse fourier transform
def compute_inverse_fourier_transform(fourier_transform, fourier_matrix):
    output = torch.matmul(fourier_transform, fourier_matrix.T)
    return output

def fourier_existing_library(samples, check_sample_size = 10):
    fourier_transform = torch.fft.fft(samples[:check_sample_size])
    fourier_stack = torch.stack([fourier_transform.real, fourier_transform.imag], dim = -1)
    return fourier_stack

def find_errors(fourier_transform, fourier_existing):
    error = torch.sqrt(torch.mean((fourier_transform - fourier_existing) **2))
    print("The error between the two fourier transforms is: ", error)


def plot_song(samples):
    plt.figure()
    plt.plot(samples)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.title("Actual voice data representation")
    plt.show()

def main():
    samples_np, _ = get_song()
    samples = torch.from_numpy(samples_np)
    #plot_song(samples, sampling_rate)

    start_time = time.time()
    fourier_matrix = create_fourier_weights(samples, 20000)
    fourier_transform = compute_fourier_transform(samples, fourier_matrix, 20000)
    end_time = time.time()
    print("The time taken for the fourier transform is: ", end_time - start_time)
    
    start_time = time.time()
    fourier_existing  = fourier_existing_library(samples, 20000) 
    end_time = time.time()
    print("The time taken for the fourier transform using existing library is: ", end_time - start_time)

    find_errors(fourier_transform, fourier_existing)
    

if __name__ == '__main__':
    main()
