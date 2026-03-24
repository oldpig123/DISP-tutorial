import numpy as np
import matplotlib.pyplot as plt

#tunable constants
L = 20
amplitude = 1

# signal generation
# L means the length of each part of the signal
# space between each part is also L
def signal_generation(L, amplitude):
    # square wave
    sqare = np.ones(L) * amplitude
    # positive slope, from -amplitude to amplitude
    pos_ramp = np.linspace(-amplitude, amplitude, L)
    # negative slope, from amplitude to -amplitude
    neg_ramp = np.linspace(amplitude, -amplitude, L)
    # sine wave
    n = np.arange(L)
    sine = np.sin(2*np.pi*n/L) * amplitude

    # glue them together
    # leading zero padding with length L
    final_signal = np.concatenate([np.zeros(L), sqare, np.zeros(L), pos_ramp, np.zeros(L), neg_ramp, np.zeros(L), sine, np.zeros(L)])
    return final_signal

# match finding
def match_finding(signal, target):
    # time reversed target
    target_rev = target[::-1]
    # convolution
    result = np.convolve(signal, target_rev, mode='same')
    # find the index of the maximum value
    max_index = np.argmax(result)
    return result, max_index


# plot the signal
signal = signal_generation(L, amplitude)

# target signal
target = np.linspace(-amplitude, amplitude, L)

# find the match
result, max_index = match_finding(signal, target)

# plot the signal in same figure
plt.figure(figsize=(12, 4), dpi = 300)
plt.subplot(3, 1, 1)
plt.stem(signal)
plt.title("signal")
plt.subplot(3, 1, 2)
# 0 padding at tail to make it same length as signal
plt.stem(np.concatenate([target, np.zeros(len(signal) - len(target))]))
plt.title("target")
plt.subplot(3, 1, 3)
plt.stem(result)
plt.title("result with max index at " + str(max_index))
#tight layout
plt.tight_layout()
plt.savefig("exercise/DISP_3/match_finding.png")
plt.clf()
