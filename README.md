# DISP Course: Project Portfolio
This repository contains my implementation and technical notes for the Digital Information Signal Processing (DISP) course.

---

## 📚 Tutorial Index
| Tutorial File | Topic | Status | Scripts |
| :--- | :--- | :--- | :--- |
| `multimedia_python.pptx` | Multimedia R/W & FFT | ✅ Complete | `multi_media_r_w_1, 2, 3.py` |
| `DISP_1_new.pptx` | DISP Fundamentals | ⏳ Pending | - |

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

---
