import unittest
import Visualise_Fourier as vf
import numpy as np

class TestFourier(unittest.TestCase):
    # This is to check if the values are correct.
    def _compare_values_(self, x, y, epi = 0.0001):
        if len(x) != len(y):
            return False
        for i in range(0, len(x)):
            if np.abs(x[i] - y[i]) > epi:
                print(str(i) +  " " + str(x[i]) + " "+  str(y[i]) + "Error found")
                return False
        return True

    # Checks if the values of fft and ifft are almost the same
    def test_fft_ifft(self):
        print("Checking if the symmentric replacement works")
        y_extra, yf = vf.check_fft_ifft()
        self.assertTrue(self._compare_values_(y_extra, yf))

    def _no_imag_check_(self, ifft_values, epsilon = 0.00001):
        for value in ifft_values:
            if np.abs(value.imag) > epsilon:
                return False
        return True

    # Checks if the imaginary components of ifft is zero
    def test_ifft_values(self):
        print("Checking if there is no imaginary part in the inverse transform")
        p = vf.Plotting()
        samples, sampling_rate = p.plot_handling()
        y_extra, yf = vf.check_fft_ifft()
        ifft_values = p.find_inverse_fft(yf, sampling_rate)
        self.assertTrue(self._no_imag_check_(ifft_values))

    def _conversion_check_(self, actual_val, conv_val, epsilon = 0.0001):
        for i in range(len(actual_val)):
            if abs(actual_val[i].real - conv_val[i].real) > epsilon:
                return False
            if abs(actual_val[i].imag - conv_val[i].imag) > epsilon:
                return False
        return True

    # Convert the complex number to amplitude-phase and back to original format
    def test_angle_imag_conv(self):
        print("Checking if the conversion to amplitude and phase and back works")
        p = vf.Plotting()
        samples, sampling_rate = p.plot_handling()
        _, actual_val,_ = p.find_fft(samples, sampling_rate)
        ampl, phase, conv_val = p.ampl_phase_back(actual_val)        
        self.assertEqual(len(actual_val), len(conv_val))
        self.assertTrue(self._conversion_check_(actual_val, conv_val))

    # Get the amplitude and frequency of the FFT and check if it working properly
    def test_freq_imag_conv(self):
        print("Checking the conversion to frequency and back works")
        p = vf.Plotting()
        samples, sampling_rate = p.plot_handling()
        N = len(samples)
        T = 1/ sampling_rate
        _, actual_val,_ = p.find_fft(samples, sampling_rate)
        ampl, freq, conv_val = p.ampl_freq_back(actual_val, N, T)
        self.assertEqual(len(actual_val), len(conv_val))

        print(actual_val[:10])
        print(conv_val[:10])


        self.assertTrue(self._conversion_check_(actual_val, conv_val))

    def _check_consistency_(self, y_np_array, samples, epsilon = 0.0001):
        if len(y_np_array) != len(samples):
            return False
        else:
            for i in range(0, len(y_np_array)):
                if y_np_array[i] - samples[i] > epsilon:
                    return False
        return True

    def test_final_check(self):
        print("Checking if the final value derived and the actual sample is the same")
        p = vf.Plotting()
        samples, sampling_rate = p.plot_handling()
        # Convert the normal sample to fft wave
        y_extra, yf = vf.check_fft_ifft()
        # Convert the FFT signal received back to fourier wave
        y = p.find_inverse_fft(yf, sampling_rate)
        y_inv  = p.convert_to_real(y)
        y_np_array = np.array(y_inv, np.float32)

        self.assertTrue(self._check_consistency_(y_np_array, samples))

if __name__ == '__main__':
    unittest.main()