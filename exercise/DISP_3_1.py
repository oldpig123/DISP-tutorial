import numpy as np 
import matplotlib.pyplot as plt

# signal generation
#  x[n] = 1 for 0 <= n <= 50
#  x[n] = 0 for 50 < n <= 100
def signal_generation():
    n = np.arange(0, 101)
    x = np.zeros(len(n))
    x[(n>=0) & (n<=50)] = 1
    x[(n>50) & (n<=100)] = 0
    return x

# gaussian noise
# assume the noise is same as the slide #2
def noise_func(n, An):
    return An * (np.random.rand(len(n)) - 0.5)

# bilateral filter
# assume k1 and k2 value follow slide page 7
def bilateral_filter(x, L, k1 = 0.3, k2 = 5):
    C = C_function(x, L,k1,k2)
    y = np.zeros(len(x))
    # from n = L to len(x) - L - 1
    # prevent index out of bound
    for n in range(len(x)):
        # m = n - L to n + L, with boundary check
        for m in range(max(0, n - L), min(len(x), n + L + 1)):
            y[n] += np.exp(-k1 * ((n - m)**2)) * np.exp(-k2 * ((x[n] - x[m])**2)) * x[m]
        y[n] = y[n] * C[n]
    return y

#C[n] = 1 / sum(exp(-k1 * ((n - m)**2)) * exp(-k2 * ((x[n] - x[m])**2))) from m = n - L to n + L
def C_function(x, L, k1 = 0.3, k2 = 5):
    C = np.zeros(len(x))
    # m = n - L
    for n in range(len(x)):
        sum = 0
        # m = n - L to n + L, with boundary check
        for m in range(max(0, n - L), min(len(x), n + L + 1)):
            sum += np.exp(-k1 * ((n - m)**2)) * np.exp(-k2 * ((x[n] - x[m])**2))
        C[n] = 1 / sum
    return C

# x-axis
n = np.arange(0, 101)
#clean signal
x = signal_generation()
# add noise
noise = noise_func(n, 0.1)
y = x + noise

# plot clean signal and signal with noise
plt.figure(figsize=(12, 6), dpi = 300)
plt.subplot(1, 3, 1)
plt.plot(n, x)
plt.title("clean signal")
plt.subplot(1, 3, 2)
plt.plot(n, y)
plt.title("signal with noise")

# apply bilateral filter
L = 5
k1 = 0.3
k2 = 5
y1 = bilateral_filter(y, L, k1, k2)

# plot signal with noise and signal after bilateral filter
plt.subplot(1, 3, 3)
plt.plot(n, y1)
plt.title("signal after bilateral filter")
plt.savefig("exercise/DISP_3/signal_after_bilateral_filter.png")
plt.clf()