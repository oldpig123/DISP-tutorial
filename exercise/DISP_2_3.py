import numpy as np
import matplotlib.pyplot as plt

# tunable constants
An = 0.5 # noise amplitude factor
sigma = 1.0

# signal generation
#  x[n] = 1 for -10 <= n <= 20, 50 <= n <= 80
#  x[n] = 0 for -30 <= n < -10, 20 < n < 50, 80 < n <= 100
def signal_generation():
    n = np.arange(-30, 101)
    x = np.zeros(len(n))
    x[((n>=-10) & (n<=20)) | ((n>=50) & (n<=80))] = 1
    x[((n>=-30) & (n<-10)) | ((n>20) & (n<50)) | ((n>80) & (n<=100))] = 0
    return x

# noise function
def noise_func(n, An):
    return An * (np.random.rand(len(n)) - 0.5)

# edge filter h[n] = -C * sgn[n] * exp(-sigma * abs(n))
# C = 1/sum(exp(-sigma * abs(n))) for n from 1 to len(x)
def edge_filter(x, sigma):
    n_h = np.arange(len(x)) - len(x)//2
    C = C_function(x, sigma)
    h = -C * np.sign(n_h) * np.exp(-sigma * abs(n_h))    
    return h
    

def C_function(x, sigma):
    sum = 0
    for i in range(1, len(x)):
        sum += np.exp(-sigma * abs(i))
    return 1 / sum
        

x = signal_generation()

# test with 2 different An and 2 different sigma
An_list = [0.1, 0.5]
sigma_list = [0.1, 1.0, 5.0]
n = np.arange(-30, 101)

plt.figure(figsize=(24, 18), dpi = 300)
plt.subplot(3,4,1)
plt.stem(n, x)
plt.title("original signal")
plt.subplot(3,4,2)
x2 = np.convolve(x, edge_filter(x, sigma_list[0]), mode='same')
plt.stem(n, x2)
plt.title("no noise, sigma="+str(sigma_list[0]))
plt.subplot(3,4,3)
x3 = np.convolve(x, edge_filter(x, sigma_list[1]), mode='same')
plt.stem(n, x3)
plt.title("no noise, sigma="+str(sigma_list[1]))
plt.subplot(3,4,4)
x4 = np.convolve(x, edge_filter(x, sigma_list[2]), mode='same')
plt.stem(n, x4)
plt.title("no noise, sigma="+str(sigma_list[2]))
for An in An_list:
    # noise
    noise = noise_func(n, An)
    # signal with noise
    x1 = x + noise
    plt.subplot(3,4,An_list.index(An)*4+5)
    plt.stem(n, x1)
    plt.title("An="+str(An)+", no filter apply")
    for sigma in sigma_list:
        # signal with noise and filter
        x2 = np.convolve(x1, edge_filter(x, sigma), mode='same')
        # plot the signal with noise #index(An) and filter #index(sigma)
        plt.subplot(3,4,An_list.index(An)*4+sigma_list.index(sigma)+1+5)
        plt.stem(n, x2)
        plt.title("An="+str(An)+", sigma="+str(sigma))

# save them in a picture
plt.tight_layout(pad=2.0)
plt.savefig("exercise/DISP_2/edge_filter.png")
plt.clf()