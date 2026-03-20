import scipy.io.wavfile as wav
import numpy as np
import scipy.fftpack as fft
import matplotlib.pyplot as plt
import os

# Check if file exists
wav_path = "VocalSignal/Alarm01.wav"
if not os.path.exists(wav_path):
    print(f"Error: {wav_path} not found.")
    import sys
    sys.exit(1)

fs, data = wav.read(wav_path)
channel0 = data[:, 0]
num_frame = len(channel0)
raw_fft = abs(fft.fft(channel0))

# Pre-calculate common factors
T = num_frame / fs  # Duration in seconds

# Experiments
v1 = raw_fft / fs / (2**15)  # Current version
v2 = raw_fft / (2**15)       # Only bit-depth
v3 = raw_fft / fs            # Only sampling rate
v4 = raw_fft / num_frame     # Only sample count

print(f"Max Amplitude with V1 (/fs /32768): {np.max(v1):.2f}")
print(f"Max Amplitude with V2 (/32768):     {np.max(v2):.2f}")
print(f"Max Amplitude with V3 (/fs):        {np.max(v3):.2f}")
print(f"Max Amplitude with V4 (/N):         {np.max(v4):.2f}")

# Segmented check (maybe tutorial only uses 1st second?)
N_seg = min(len(channel0), 22050)
seg_fft = abs(fft.fft(channel0[:N_seg]))
v5 = seg_fft / (2**15)
v6 = seg_fft / fs
print(f"Max Amplitude Segment (1s) /32768:   {np.max(v5):.2f}")
print(f"Max Amplitude Segment (1s) /fs:      {np.max(v6):.2f}")

# Plotting Comparison
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes[0,0].plot(v1); axes[0,0].set_title("V1: /fs /2^15")
axes[0,1].plot(v2); axes[0,1].set_title("V2: /2^15")
axes[1,0].plot(v3); axes[1,0].set_title("V3: /fs")
axes[1,1].plot(v4); axes[1,1].set_title("V4: /N")

output_dir = "exercise/multi_media_r_w_1"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(f"{output_dir}/Experiment_Results.png")
print(f"\nPlot saved to {output_dir}/Experiment_Results.png")
