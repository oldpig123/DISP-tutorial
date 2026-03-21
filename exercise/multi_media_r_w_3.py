import cv2
import numpy as np
cap = cv2.VideoCapture("exercise/test.mp4")
if not cap.isOpened():
    print("Cannot open camera")
    exit()
# Get the original speed of the video
fps = cap.get(cv2.CAP_PROP_FPS)
delay = int(1000 / fps)
frame_num = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    cv2.imshow("frame", frame)
    key =cv2.waitKey(delay)

    if key == ord("q"):
        break
    if key == ord("s"):
        cv2.imwrite(f"exercise/multi_media_r_w_3/test_{frame_num}.bmp", frame)
        frame_num += 1

cap.release()
cv2.destroyAllWindows()

cap = cv2.VideoCapture("exercise/test.mp4")
if not cap.isOpened():
    print("Cannot open camera")
    exit()
# Get the original speed of the video
fps = cap.get(cv2.CAP_PROP_FPS)
delay = int(1000 / fps)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
output1 = cv2.VideoWriter("exercise/multi_media_r_w_3/output1.avi", fourcc, fps, (width, height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    frame = cv2.flip(frame,0)
    output1.write(frame)
    cv2.imshow("frame", frame)
    key =cv2.waitKey(delay)
    if key == ord("q"):
        break

cap.release()
output1.release()
cv2.destroyAllWindows()