# DISP Course: Project Portfolio
This repository contains my implementation and technical notes for the Digital Information Signal Processing (DISP) course.

---

## 📚 Tutorial Index
| Tutorial File | Topic | Status | Scripts |
| :--- | :--- | :--- | :--- |
| `multimedia_python.pptx` | Multimedia R/W & FFT | ✅ Complete | `multi_media_r_w_1, 2, 3.py` |
| `DISP_1_new.pptx` | DISP Fundamentals | ✅ Complete | `exercise/DISP_1_1.py`, `1_2.py`, `1_3.py` |

---

# 🎮 Tutorial 1: Multimedia Python (`multimedia_python.pptx`)
Implementation of Slides 3 - 22 involving Audio, Image, and Video processing.

## 📝 Implementation Notes

### FFT Normalization (Exercise 1)
- **Discrepancy**: Slide 5 suggests dividing by `fs * 2**15`, but Slide 6 plot requires only dividing by `fs` to reach the ~2345 peak.
- **Solution**: Omitted `2**15` division in `multi_media_r_w_1.py`.

### Audio Playback & SSH
- **Discrepancy**: Slide 7 ignores raw `int16` data type from Slide 3.
- **Solution**: Explicitly normalized to floats before scaling back by `32767` for `simpleaudio`.
- **Note**: Placed file-saving above playback to avoid script termination on SSH segmentation faults.

### Image Processing (Exercise 2)
- **Problem**: `plt.show()` fails via virtual environment due to "Double Qt" conflicts.
- **Solution**: Prioritized `cv2.imshow` for interactive use and `imwrite/savefig` for result storage.
- **Learning**: Mastered float vs integer `imshow` logic (The 255-division rule).

### Video Processing (Exercise 3)
- **Modification**: Replaced Matplotlib's manual "Save" button with a custom **Keyboard Listener** ('s' key) in OpenCV for better reliability in non-GUI environments.
- **Final Result**: Created `output1.avi` featuring a vertically flipped mirror of the W3Schools sample video.

---

# 📉 Tutorial 2: DISP Basics (`DISP_1_new.pptx`)
Implementation of Slides 3 - 40 involving Edge Detection and Signal Metrics.

## 📝 Implementation Notes

### 1. Edge Detection (Exercise 1, Slides 3-9)
We implemented six directional filters: **Laplacian**, **Horizontal Sobel**, **Vertical Sobel**, and **Diagonal Sobels (45°/135°)**.

- **The "Student" Approach**: We first implemented the Laplacian manually using nested loops. This proved that we understood the mathematical "Stencil" (Kernel) sliding over the image.
- **The "Border Problem"**: When sliding a 3x3 kernel, the window "hangs off" the edge of the image. We solved this by adjusting the loop ranges to `range(1, height-1)`, which skips the 1-pixel border.
- **The "Bit-Depth Trap"**: 
    - **Issue**: Gradients produce negative numbers (e.g., Light-to-Dark transitions).
    - **Trap**: Standard 8-bit images (`uint8`) cannot store negatives—they "wrap around" (e.g., -10 becomes 246), creating noise.
    - **Solution**: We performed all calculations in **`CV_64F` (64-bit float)** and used **`np.abs(result)`** before converting back to `uint8`.
- **Normalization Constants**: We followed the Tutorial's Slide 5-9 formulas exactly by dividing the result of Sobel by **`4.0`** and the Laplacian by **`8.0`**.
- **Visibility (`C * abs(E)`)**: Because normalized edges are faint, we used a scaling constant `C = 10.0` or `15.0` to make the outlines high-contrast.

### 2. YCbCr Brightness Adjustment (Exercise 2, Slides 27-29)
We implemented a brightness controller that works in the **YCbCr** colorspace to avoid the color distortion (washout) seen in BGR-only lightening.

- **The "Transpose Identity"**: 
    - **Problem**: Slide 22 shows $\mathbf{YCC} = \mathbf{M} \cdot \mathbf{BGR}$ (Matrix on left). But NumPy treats a 2D pixel as a **Row Vector**.
    - **Solution**: According to the identity $(\mathbf{M} \mathbf{v})^T = \mathbf{v}^T \mathbf{M}^T$, we placed the image on the left and transposed the matrix: `np.dot(Image, Matrix.T)`.
- **The 128-Shift Logic**: 
    - **Issue**: Standard Cb/Cr storage uses a `+128` offset to keep values positive for 8-bit files.
    - **Insight**: For manual math, we stayed in **float64** without the shift. This kept the color data "Pure" (allowing negative values) until the final BGR reconstruction step, avoiding the "Invalid sqrt" and "Data Loss" traps.
- **Color Order Strategy**: We stacked channels as `(r, g, b)` to match Slide 22's matrices, then flipped them back to `(b, g, r)` at the end for OpenCV compatibility.

### 3. Signal Metrics (Exercise 3, Slides 32-34)
We implemented NRMSE and PSNR to measure the mathematical "Distance" between the original and processed images.

- **The 3-Layer Loop**: We implemented the summation as a triple-loop (Height x Width x Color) to ensure mathematical alignment with the theory. 
- **The "Data Type" Safety**: We learned to cast to `float` before subtraction to prevent `uint8` wrap-around errors. 
- **Verifying "Reasonableness"**:
    - **Laplacian (7.1 dB PSNR)**: Correctly indicates a massive difference between a photo and its edges.
    - **Darken (18.1 dB PSNR)**: Higher quality than lightening (14.2 dB) in this test case.

---
