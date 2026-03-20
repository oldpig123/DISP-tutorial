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

## Audio Playback and SSH Note (Exercise 1)
There is another discrepancy regarding audio playback on Slide 7 of `multimedia_python.pptx`.

- **Slide 3 (File Reading)**: Uses `scipy.io.wavfile.read()`, which natively loads a 16-bit WAV file as an array of raw integers (`np.int16`), in the range `[-32768, 32767]`.
- **Slide 7 (Playback)**: Instructs the student to convert the data for playback using:
  ```python
  wave_data = (2**15 - 1) * wave_data
  wave_data = wave_data.astype(np.int16)
  ```

**Explanation**: 
The logic on Slide 7 assumes that `wave_data` is a **normalized float** in the range `[-1.0, 1.0]`. If you multiply the original raw `int16` array by `32767`, it causes an extreme integer overflow resulting in a broken audio signal. 
The tutorial author likely normalized the audio to floats off-screen between Slide 3 and Slide 7 (e.g., `wave_data = wave_data / 2**15`). In our implementation, we resolve this by performing the Slide 7 multiplication on our explicitly peak-normalized float variable (`data_peak_norm`) to safely scale it back for playback.

### SSH Segmentation Fault Issue
When running `simpleaudio.play_buffer` on a remote Linux server via SSH without a dedicated audio device/driver open, the `simpleaudio` C-library will often successfully finish playing the audio buffer (via X11/PulseAudio forwarding) but hit a **Segmentation Fault (Exit Code 139)** during cleanup (`play_obj.wait_done()`). 

Because this forcefully kills the Python script upon completion, we must place any file-saving code (`wav.write(...)`) **above** the audio playback code so that your outputs are safely written to disk before the playback termination crashes the script.
