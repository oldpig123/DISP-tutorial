# DISP-tutorial

## FFT Normalization Note (Exercise 1)
In the multimedia python tutorial (`multimedia_python.pptx`), there is a discrepancy between the code provided on Slide 5 and the output shown on Slide 6 regarding the FFT amplitude scaling of `Alarm01.wav`.

- **Slide 5 (Code)**: Suggests normalizing the FFT data by dividing both by the sampling frequency (`fs`) and the maximum 16-bit integer value (`2**15` or `32768`).
  Example snippet:
  ```python
  fft_data = abs(fft(wave_data[:,0])) / fs
  fft_data = fft_data / 2**15
  ```
- **Slide 6 (Plot)**: Shows a peak amplitude between 2000 and 2500.

**Explanation**: 
Applying both divisions results in a peak amplitude of `~0.07` for `Alarm01.wav`. To reproduce the exact plot shown on Slide 6 (which has a peak of `~2345`), we must **omit** the division by `2**15` and only divide the FFT by `fs`. 

The `fft_data / 2**15` line was likely intended as a best practice to normalize the amplitude to a `[0, 1]` range, but the tutorial author did not apply it when generating the figure on the subsequent slide.

In our implementation (`exercise/multi_madia_r_w_1.py`), we have commented out the `/ 2**15` division to ensure our output plot precisely matches the tutorial's reference image while preserving the mathematical intent of the first normalization step.
