import scipy.io.wavfile as wav
import numpy as np
import matplotlib.pyplot as plt

fs, data = wav.read("VocalSignal/Alarm01.wav")

data_peak_norm = data/np.max(np.abs(data))

num_frame = len(data)
num_channel_1 = int(data.size / num_frame)
num_channel_2 = data.shape[1]

print(fs,num_frame, num_channel_1, num_channel_2)

time = np.arange(0, num_frame/fs, 1/fs)
plt.plot(time, data_peak_norm)
plt.savefig("exercise/multi_media_r_w_1/Alarm01_waveform.png")
plt.clf()

import scipy.fftpack as fft

fft_data = abs(fft.fft(data[:,0]))/fs
# fft_data = fft_data/2**15  # Removed to match tutorial amplitude (~2300)

freq = fft.fftfreq(num_frame, 1/fs)

# following is what tutorial mentioned
# n0 = int(np.ceil(num_frame/2))
# fft_data_1 = np.concatenate((fft_data[n0:], fft_data[:n0]))
# freq = np.concatenate([range(n0-num_frame,0), range(0,n0)]) * fs/num_frame


# import scipy.fftpack as fft

# # Shift the data so 0Hz is in the middle
fft_data_centered = fft.fftshift(fft_data)
freq_centered = fft.fftshift(freq)

plt.plot(freq_centered, fft_data_centered)
plt.xlim([-800, 800])
plt.savefig("exercise/multi_media_r_w_1/Alarm01_fft.png")

import simpleaudio as sa
wav.write("exercise/multi_media_r_w_1/Alarm01_new.wav", fs, data)
print("Alarm01_new.wav is saved.")


import pyaudio
pa = pyaudio.PyAudio()
fs = 44100
chunk = 1024
stream = pa.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=fs,
    input=True,
    frames_per_buffer=chunk
)

vocal = []
count = 0
print("Recording...")
while count < 200:
    audio_data = stream.read(chunk)
    vocal.append(audio_data)
    count += 1

# Join the recording chunks and convert to numpy for saving
vocal_bytes = b''.join(vocal)
vocal_np = np.frombuffer(vocal_bytes, dtype=np.int16)

wav.write("exercise/multi_media_r_w_1/test_record.wav", fs, vocal_np)
print("test_record.wav is saved.")
stream.close()

# play the recorded audio (vocal_bytes is the correct buffer format)
print("Playing...")
play_obj = sa.play_buffer(vocal_bytes, 1, 2, fs)
play_obj.wait_done()

n_byte = 2
play_data = (2**15 - 1)*data_peak_norm

play_data = play_data.astype(np.int16)
play_obj = sa.play_buffer(play_data, num_channel_1, n_byte, 22050)
play_obj.wait_done()