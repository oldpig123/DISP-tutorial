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

## Image Processing and Display Note (Exercise 2)
When performing image processing tasks from Slides 11-17, interactive display functions like `cv2.imshow()` and `plt.show()` may behave unexpectedly due to environment restrictions.

### "Double Qt" Conflict
In a Python virtual environment (like the one managed by `uv`), there is often a conflict between the **private Qt version** bundled inside OpenCV (`cv2`) and the **public Qt version** needed by Matplotlib (`PyQt5`).
- **OpenCV (`cv2`)**: Bundles its own C++ Qt shared libraries. It can often open its own `imshow` window even when other libraries fail.
- **Matplotlib**: Requires a separate interactive backend (like `PyQt5`) to be explicitly installed in the virtual environment.

### XCB Plugin Errors
Even on a physical machine, running these GUI functions through a remote terminal or a virtual environment can trigger errors like `Could not load the Qt platform plugin "xcb"`. This occurs when the Python Qt package cannot find required Linux system libraries (e.g., `libxcb-xinerama0`) or when there is a mismatch in X11/Wayland display permissions.

### Interactive Display Priority
Based on local testing on the physical machine:
- **`cv2.imshow()` and `cv2.waitKey()`**: Functions correctly and is the preferred way to view images interactively.
- **`plt.show()`**: Continuously fails for image display due to the "Double Qt" conflict (using the non-interactive `Agg` backend).

**Decision**: In our exercise scripts (e.g., `multi_media_r_w_2.py`), we prioritize `cv2.imshow()` for interactive viewing and skip `plt.show()` for images to prevent backend errors, while still keeping `imwrite`/`savefig` for permanent result storage.
