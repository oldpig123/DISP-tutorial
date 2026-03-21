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
*Notes for next section...*

- [ ] (Waiting for Discovery phase)
