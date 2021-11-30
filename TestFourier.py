import unittest
import Visualise_Fourier as vf
import numpy as np

class TestFourier(unittest.TestCase):
    # This is to check if the values are correct.
    def _compare_values_(self, x, y, epi = 0.001):
        if len(x) != len(y):
            return False
        for i in range(0, len(x)):
            if np.abs(x[i] - y[i]) > epi:
                print(str(i) +  " " + str(x[i]) + " "+  str(y[i]) + "Error found")
                return False
        return True

    # Checks if the values of fft and ifft are almost the same
    def test_fft_ifft(self):
        y_extra, yf = vf.check_fft_ifft()
        self.assertTrue(self._compare_values_(y_extra, yf))

    def _no_imag_check_(self, ifft_values, epsilon = 0.00001):
        for value in ifft_values:
            if np.abs(value.imag) > epsilon:
                return False
        return True

    # Checks if the imaginary components of ifft is zero
    def test_ifft_values(self):
        p = vf.Plotting()
        samples, sampling_rate = p.plot_handling()
        y_extra, yf = vf.check_fft_ifft()
        ifft_values = p.find_inverse_fft(yf, sampling_rate)
        self.assertTrue(self._no_imag_check_(ifft_values))

    def _conversion_check_(self, actual_val, conv_val, epsilon = 0.0001):
        for i in range(len(actual_val)):
            if actual_val[i].real - conv_val[i].real > epsilon:
                return False
            if actual_val[i].imag - conv_val[i].imag > epsilon:
                return False
        return True

    def test_angle_imag_conv(self):
        p = vf.Plotting()
        samples, sampling_rate = p.plot_handling()
        _, actual_val,_ = p.find_fft(samples, sampling_rate)
        ampl, phase, conv_val = p.ampl_phase_back(actual_val)        
        self.assertEquals(len(actual_val), len(conv_val))
        self.assertTrue(self._conversion_check_(actual_val, conv_val))

if __name__ == '__main__':
    unittest.main()