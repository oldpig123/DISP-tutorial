import scipy.io.wavfile as wav
import numpy as np
import matplotlib.pyplot as plt

fs, data = wav.read("VocalSignal/Alarm01.wav")
# fs is sampling rate, data is the audio data, which is a 2D array 
# the first dimension is the number of samples, the second dimension is the number of channels
# length of data is the number of samples, which is the number of samples in each channel
# so the physical length of the audio is len(data)/fs
# which 1/fs is the time interval between two samples, or sampling period

mono_data = data[:,0]
num_frame = len(mono_data)

fft_data = np.fft.fft(mono_data)
# freq = m * fs / num_frame
freq = np.arange(num_frame) * fs / num_frame

# shift the fft data
fft_data_shifted = np.fft.fftshift(fft_data)
freq_centered = np.arange(-num_frame/2, num_frame/2) * fs / num_frame
# freq_centered = np.linspace(-fs/2, fs/2, num_frame)

# save the fft diagram as a picture
plt.plot(freq_centered, abs(fft_data_shifted))
plt.savefig("exercise/DISP_2/fft_diagram.png")
