import cv2

def extract_frames(video_source):
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        raise IOError("Could not open video source.")
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    if frame_rate == 0:
        frame_rate = 30.0
    frames = []
    timestamps = []
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
        time_sec = i / frame_rate
        frames.append(frame)
        timestamps.append(time_sec)
    cap.release()
    return frames, frame_rate, timestamps
