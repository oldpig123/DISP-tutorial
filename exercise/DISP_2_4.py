import numpy as np
import matplotlib.pyplot as plt

# signal generation
#  x[n] = 0.1*n for -50<= n <= 100
def signal_generation():
    n = np.arange(-50, 101)
    x = 0.1 * n
    return x

# noise function
def noise_func(n, An):
    return An * (np.random.rand(len(n)) - 0.5)

# x1[n] = x[n] + noise
def add_noise(x, An):
    noise = noise_func(x, An)
    x1 = x + noise
    return x1

# smoother filter
# h[n] = C * exp(-sigma * abs(n)) for abs(n) <= len(x)
# C = 1/sum(exp(-sigma * abs(n))) for n from 1 to len(x)
def C_function(x, sigma):
    sum = 0
    for i in range(1, len(x)):
        sum += np.exp(-sigma * abs(i))
    return 1 / sum

def smoother_filter(x, sigma):
    n_h = np.arange(len(x)) - len(x)//2
    C = C_function(x, sigma)
    h = C * np.exp(-sigma * abs(n_h))
    return h

x = signal_generation()

# test with 2 different An and 2 different sigma
An_list = [0.1, 0.5, 1.0]
sigma_list = [0.1, 1.0, 5.0]
n = np.arange(-50, 101)

# save the filter for different sigma in a picture
# save as exercise/DISP_2/smoother_filter.png
plt.figure(figsize=(24, 18), dpi = 300)
plt.subplot(1,3,1)
plt.stem(n, smoother_filter(x, sigma_list[0]))
plt.title("sigma="+str(sigma_list[0]))
plt.subplot(1,3,2)
plt.stem(n, smoother_filter(x, sigma_list[1]))
plt.title("sigma="+str(sigma_list[1]))
plt.subplot(1,3,3)
plt.stem(n, smoother_filter(x, sigma_list[2]))
plt.title("sigma="+str(sigma_list[2]))
plt.savefig("exercise/DISP_2/smoother_filter.png")
plt.clf()

plt.figure(figsize=(24, 18), dpi = 300)
plt.subplot(4,4,1)
plt.stem(n, x)
plt.title("original signal")
plt.subplot(4,4,2)
x2 = np.convolve(x, smoother_filter(x, sigma_list[0]), mode='same')
plt.stem(n, x2)
plt.title("no noise, sigma="+str(sigma_list[0]))
plt.subplot(4,4,3)
x3 = np.convolve(x, smoother_filter(x, sigma_list[1]), mode='same')
plt.stem(n, x3)
plt.title("no noise, sigma="+str(sigma_list[1]))
plt.subplot(4,4,4)
x4 = np.convolve(x, smoother_filter(x, sigma_list[2]), mode='same')
plt.stem(n, x4)
plt.title("no noise, sigma="+str(sigma_list[2]))
for An in An_list:
    # noise
    noise = noise_func(n, An)
    # signal with noise
    x1 = x + noise
    plt.subplot(4,4,An_list.index(An)*4+5)
    plt.stem(n, x1)
    plt.title("An="+str(An)+", no filter apply")
    for sigma in sigma_list:
        # signal with noise and filter
        x2 = np.convolve(x1, smoother_filter(x, sigma), mode='same')
        # plot the signal with noise #index(An) and filter #index(sigma)
        plt.subplot(4,4,An_list.index(An)*4+sigma_list.index(sigma)+1+5)
        plt.stem(n, x2)
        plt.title("An="+str(An)+", sigma="+str(sigma))

# save them in a picture
plt.tight_layout(pad=2.0)
plt.savefig("exercise/DISP_2/smoother_filter_applied.png")
plt.clf()




    
