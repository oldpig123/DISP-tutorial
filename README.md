# DISP Course: Project Portfolio
This repository contains my implementation and technical notes for the Digital Information Signal Processing (DISP) course.

---

## 📚 Tutorial Index
| Tutorial File | Topic | Status | Scripts |
| :--- | :--- | :--- | :--- |
| `multimedia_python.pptx` | Multimedia R/W & FFT | ✅ Complete | `exercise/multi_media_r_w_1, 2, 3.py` |
| `DISP_1_new.pptx` | DISP Fundamentals | ✅ Complete | `exercise/DISP_1_1.py`, `1_2.py`, `1_3.py` |
| `DISP_2_new.pptx` | Discrete Fourier Transform | ✅ Complete | `exercise/DISP_2_1, 2, 3, 4.py` |
| `DISP_3_new.pptx` | Advanced Image Processing | ✅ Complete | `exercise/DISP_3_1.py`, `3_2.py`, `3_4.py` |
| `DISP_4_new.pptx` | Advanced Topics I | 🏃 In Progress | `exercise/DISP_4_1.py` |

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

# 🌊 Tutorial 3: Discrete Fourier Transform (`DISP_2_new.pptx`)
Advanced Signal Analysis and Frequency Domain Filtering.

## 📝 Implementation Notes

### 1. Structural Similarity Index (SSIM) (Slide 23)
Expansion of the metrics suite to include human-centric visual comparison.

- **The "Structural" Advantage**: Unlike PSNR (which only sees individual pixel "Noise"), SSIM measures **Luminance**, **Contrast**, and **Structure**. 
- **The "Lighten" Paradox**: Our `lighten_cv` image had a "Poor" PSNR of ~14 dB, but a "High" SSIM of **0.92**. This proves that while the brightness changed (MSE error), the *textures and shapes* of the peppers were perfectly preserved.
- **Implementation Strategy**:
    - **Total Variance/Covariance**: Calculated via three-layer loops (H x W x C) for absolute bit-depth safety and clarity.
    - **Stability Constants**: Used $C_1=255$ and $C_2=255$ (derived from the $c_1 = \sqrt{1/L}$ tutorial suggestion) to ensure robust division.
- **Trend Verification**:
    - **Laplacian (SSIM 0.004)**: Correctly identifies near-zero similarity between a photo and its outlines.
    - **Darken (SSIM 0.82)**: Shows significant structural degradation compared to lightening, likely due to increased "Clipping" of dark textures.

### 2. WAV Spectrum Analysis (Slide 23)
Spectral decomposition of audio signals using the Fast Fourier Transform (FFT).

- **Frequency Mapping**: Implemented the bin-to-Hz transformation: $f = m \cdot \frac{fs}{N}$.
- **Discrete Accuracy**: Prioritized `np.arange` over `np.linspace` to preserve exact $fs/N$ spectral step sizes, ensuring theoretical alignment with Discrete Signal Processing rules.
- **The `fftshift` Mechanic**: Leveraged `np.fft.fftshift` to move the zero-frequency (DC) component to the center of the plot. This provides an intuitive view of the conjugate-symmetric spectrum (negative and positive frequencies).
- **Final Result**: Generated `fft_diagram.png` showing clear spectral peaks at the characteristic frequencies of the alarm signal.

### 3. Signal Edge Detection (Slides 15-17)
Exploration of Gaussian-derivative filters for 1D signal boundary detection.

- **Impulse Response Scale**: Verified that $\sigma$ controls the filter's "vision."
    - **Small $\sigma$ (0.1)**: Long impulse response. Strong noise suppression/averaging.
    - **Large $\sigma$ (5.0)**: Short impulse response. High precision/localization.
- **Symmetry & Centering**: Implemented a zero-centered filter vector ($n \in [-L, L]$) to ensure edges are correctly aligned without time-lags.
- **The "Sum of Zero" Immunity**: Discovered that because the edge detector sums to 0, it is naturally immune to "Zero-Padding" artifacts at the boundaries if the signal is zero there (unlike the smoother).
- **Final Result**: Generated the filter shapes (`edge_filter.png`) and a 4x4 comparison grid (`edge_filter_applied.png`) demonstrating robust edge extraction under $An=1.0$ noise.

### 4. Signal Smoothing & Trend Extraction (Slide 22)
Recovery of slow-moving Trends from high-frequency Noise.

- **Scale Parameter**: Confirmed that **smaller $\sigma$** captures "Long Term Features" (heavy smoothing), while **larger $\sigma$** captures "Short Term" details (Slide 22). 
- **The "Boundary Collapse" Artefact**: Discovered that at $\sigma=0.1$, the extracted trend "collapses" toward zero at the head and tail. This is because a Smoother averages the non-zero trend with the zero-padding at the finite boundaries.
- **Normalization Discussion**: The current implementation **omits** the standard $\sum h = 1$ normalization. 
    - **Physical Effect**: This causes the trend to be "Inflated" (doubled in height) and makes the boundary artifacts look like "Modern Art." 
    - **Theoretical Note**: In professional DSP, smoothers must sum to exactly **1.0** to preserve the DC level (Brightness/Height) of the signal. Here, we've kept the high-gain results to better visualize the "Trend Extraction" struggle at low frequencies.
- **Final Result**: Generated the filter shapes (`smoother_filter.png`) and a 4x4 comparison grid (`smoother_filter_applied.png`) showing the high-gain trend recovery from $An=1.0$ noise.

---

# 🖼️ Tutorial 4: Advanced Image Processing (`DISP_3_new.pptx`)
Implementation of Slides 3 - 31 involving Non-Linear filtering and Morphology.

## 📝 Implementation Notes

### 1. Bilateral Filter (Slide 7 & 30)
Non-Linear, Edge-Preserving Smoothing.

- **Weighting Paradox**: Unlike standard convolution (Linear/Shift-Invariant), the Bilateral filter is **Adaptive**. Its weights change for every pixel based on the signal's local intensity.
- **Dual Kernels**:
    - **Space ($k_1=0.3$)**: Penalizes distance from the center pixel.
    - **Range ($k_2=5.0$)**: Penalizes intensity difference ($|x[n]-x[m]|$). This prevents the filter from "averaging across" sharp edges.
- **Boundary Handling**: Implemented **Adaptive Indexing** (`max/min`) to ensure the sliding window remains within array bounds without leaving zero-padding artifacts.
- **Final Result**: Generated `signal_after_bilateral_filter.png` showing robust noise reduction while maintaining a perfectly sharp square-wave transition.

---

### 2. Matched Filter (Exercise 2, Slide 15-16)
Implementation of pattern detection using **Cross-Correlation**.

- **Initial Approach**: Simple `np.convolve` (Direct product sum). 
    - *Weakness*: Easily fooled by high-amplitude regions (like constant white blocks).
- **Refined Approach**: **Normalized Cross-Correlation (NCC)**.
    - **Local Mean Subtraction**: For every window, we subtract the average intensity. This makes the filter **Intensity-Invariant** (it only sees the "shape", not the "brightness").
    - **Energy Normalization**: Dividing by the signal energy $\sqrt{\sum x^2}$ ensures the result stays between -1.0 and 1.0.
- **Final Result**: The detector now finds the correct ramp with a perfect **1.0 score** and ignores the high-amplitude square wave (score 0.0). Generated `match_finding_normalized_cross_correlation.png`.
- **The "Mirror" Trick**: To perform correlation using the `np.convolve` function, we must use a **Time-Reversed** version of the target pattern (`target[::-1]`).
- **Mode Comparison**:
    - **`mode='valid'`**: Returns only full-overlap results. The peak index corresponds exactly to the **Start** of the pattern.
    - **`mode='same'`**: Pads the signal to maintain length. The peak index aligns with the **Center** of the pattern.
- **Verification**: Detection of the "Positive Ramp" (indices 60-79) with $L=20$ and $A=1$ yielded a peak at index **70** (Perfect center alignment: $60 + L/2 = 70$).
- **Final Result**: Generated `match_finding.png` showing the original signal, the target, and the sharp detection peak.

### 3. Fourier Hybrid Images (Exercise 3, Slide 30)
Creating distance-dependent perception by blending the **Low-Pass** components of Lena and the **High-Pass** components of Barbara.

- **The "No-Loop" Implementation (Vectorization)**: 
    - We avoided slow Python `for` loops by using **`np.ogrid`** to create a 2D coordinate grid. 
    - This allowed us to calculate the distance of every pixel from the center in a single vectorized CPU operation.
- **The "Color Axis" consistency**:
    - **Insight**: By default, `np.fft.fft2` on a 3-channel (H, W, 3) image operates on the last two axes (Width, Channels), which scrambles the spatial data.
    - **Rule**: We explicitly used **`axes=(0, 1)`** for all four steps (`fft2`, `ifft2`, `fftshift`, `ifftshift`) to ensure the 2D transform correctly targeted the spatial dimensions while preserving the color channels.
- **Mathematical Principles (Circle vs. Diamond)**:
    - **Euclidean (Circle)**: $\sqrt{x^2 + y^2} \leq L$. Area = $\pi L^2$. Best for natural, rotationally symmetric blurring.
    - **Manhattan (Diamond)**: $|x| + |y| \leq L$. Area = $2 L^2$. This is the "Professor's Formula" from the slide diagram.
    - **Learning**: At the same $L$, the Diamond contains **~37% less information** than the Circle, resulting in a much stronger "Blur" effect.
- **Visualization (The Log Scale)**:
    - Because the DC component is millions of times stronger than the high frequencies, a raw spectrum looks black. We used **`np.log(1 + np.abs(F))`** to compress the dynamic range for human visibility.
- **Final Result**: Generated `merge_img.png` featuring a 3x3 diagnostic grid showing the spectral masks and the final "Shape-Shifting" hybrid.

---

### 4. Image Morphology (Exercise 4, Slide 31)
Implementation of **Erosion**, **Dilation**, **Opening**, and **Closing** with $k=3$ iterations.

- **Grayscale Principle**: We implemented Morphology as a **Minimum/Maximum** filter (Slide 27), allowing it to operate on 8-bit grayscale images like Lena.
- **The "Chain Rule"**: We verified that 3 iterations of a $3 \times 3$ kernel effectively creates a $7 \times 7$ window ($2k+1$).
- **Vectorization Upgrade**: 
    - **Problem**: Nested Python loops for 14M operations took over 10 seconds.
    - **Solution**: We implemented **`sliding_window_view`** to shift the loops into optimized C code.
    - **Indexing lesson**: We learned that to apply a mask to a 4D windowed array, we must use **`[:, :, kernel == 1]`** to isolate the window axes from the spatial axes.
- **Visual Interpretation**:
    - **Erosion**: Shrinks highlights (Min filter).
    - **Dilation**: Expands highlights (Max filter).
    - **Opening**: Removes small bright noise (Erode then Dilate).
    - **Closing**: Fills dark gaps and cracks (Dilate then Erode).
- **Final Result**: Generated `morphological_operations.png`.

---


---

# 🔬 Tutorial 5: Advanced Topics I (`DISP_4_new.pptx`)
Implementation of Slides 3 - 22 involving Image Restoration, PCA, and Gram-Schmidt.

## 📝 Implementation Notes

### 1. Image Restoration (Exercise 1, Slides 3-20)
Recovery of a degraded image ($y = x * k + noise$) using a regularized inverse filter (Equalizer).

- **The "Page 5" Padding Logic**:
    - **Challenge**: To perform FFT-based restoration, the kernel must be the same size as the image ($512 \times 512$).
    - **The Trap**: Placing the kernel in the center causes a spatial shift in the output.
    - **Solution**: Implemented the **Quadrant Wrapping** method from Page 5. We "split" the centered $21 \times 21$ kernel into 4 corners of the large matrix. This ensures the peak is at index `(0,0)`, preventing any phase shift (ghosting) in Lena.
- **The Equalizer (Wiener-style)**:
    - **Formula**: $\hat{X} = Y \cdot \frac{K^*}{|H|^2 + C}$.
    - **The Trade-off**: 
        - **Small $C$ (0.01)**: High sharpness but high noise amplification (looks like sandpaper).
        - **Large $C$ (0.5)**: Low noise but persistent blur (Safe but uninformative).
- **The "DC Attenuation" Discovery**:
    - **Observation**: We noticed that as $C$ increases, the whole image becomes **Darker**.
    - **Explanation**: Since our kernel sum is 1.0, its DC gain is 1.0. When $C=0.5$, the gain at the origin becomes $1 / (1 + 0.5) = 0.66$, effectively losing 33% of the image's energy.
- **Visual Stability**: 
    - **Issue**: Restoration often pushes pixel values outside the 0-255 range (e.g. negative spikes).
    - **Solution**: Implemented **`np.clip(result, 0, 255)`** and used explicit `vmin/vmax` in Matplotlib to ensure consistent brightness comparison across different parameters.
- **Final Result**: Generated `original_and_blurred_and_restored.png` featuring a 3x3 sweep of noise levels (10, 50) and regularization constants (0.01, 0.05).

---

# 🏁 Portfolio Milestone Complete
Tutorial 5 (Exercise 1) is successfully documented. Ready for PCA and Gram-Schmidt analysis.
