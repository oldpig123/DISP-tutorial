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

# match finding w/ normalized cross-correlation and local mean
# window boundary $\tau_1 = -(L/2), \tau_2 = L/2$
# window width = L
def match_finding_normalized_cross_correlation(signal, target):
    L = len(target)
    tau_1 = -L//2
    tau_2 = L//2
    
    # pad signal with L/2 zeros at both ends
    signal_pad = np.pad(signal, (L//2, L//2), mode='constant')

    # local mean of target is the mean of target
    target_mean = np.mean(target)
    target_centered = target - target_mean
    target_energy = np.sqrt(np.sum(target_centered**2))
    
    result = np.zeros(len(signal))

    for n in range(len(signal)):
        # get the window of signal
        window = signal_pad[n:n+L]
        # get the local mean of window
        window_mean = np.mean(window)
        window_centered = window - window_mean
        # get the local std deviation of window
        window_energy = np.sqrt(np.sum(window_centered**2))
        # set result = 0 if window energy =0
        if window_energy == 0:
            result[n] = 0
        else:
            result[n] = np.sum(window_centered * target_centered) / (window_energy * target_energy)
    return result, np.argmax(result)
        


# plot the signal
signal = signal_generation(L, amplitude)

# target signal
target = np.linspace(-amplitude, amplitude, L)

# find the match
# result, max_index = match_finding(signal, target)
result, max_index = match_finding_normalized_cross_correlation(signal, target) # normalized cross-correlation and local mean

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
# plt.savefig("exercise/DISP_3/match_finding.png")
plt.savefig("exercise/DISP_3/match_finding_normalized_cross_correlation.png") # normalized cross-correlation and local mean
plt.clf()
