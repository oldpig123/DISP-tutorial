import scipy.io.wavfile as wav
import numpy as np
import matplotlib.pyplot as plt

fs, data = wav.read("VocalSignal/Alarm01.wav")

num_frame = len(data)
num_channel_1 = int(data.size / num_frame)
num_channel_2 = data.shape[1]

print(fs,num_frame, num_channel_1, num_channel_2)

