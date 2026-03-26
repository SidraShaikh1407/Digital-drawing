import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import HandLandmarkerOptions
import urllib.request
import os

# ── Download model if needed ──────────────────────────────────────────────────
MODEL_PATH = "hand_landmarker.task"
if not os.path.exists(MODEL_PATH):
    print("Downloading hand_landmarker.task model (~10MB)...")
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
        MODEL_PATH
    )
    print("Download complete.")

# ── MediaPipe setup ───────────────────────────────────────────────────────────
options = HandLandmarkerOptions(
    base_options=mp_python.BaseOptions(model_asset_path=MODEL_PATH),
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.5,
    running_mode=vision.RunningMode.IMAGE
)
detector = vision.HandLandmarker.create_from_options(options)

# Hand connections to draw skeleton
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (0,9),(9,10),(10,11),(11,12),
    (0,13),(13,14),(14,15),(15,16),
    (0,17),(17,18),(18,19),(19,20),
    (5,9),(9,13),(13,17)
]

def draw_landmarks(frame, landmarks, w, h):
    """Draw hand skeleton manually without mediapipe.framework."""
    pts = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
    for a, b in HAND_CONNECTIONS:
        cv2.line(frame, pts[a], pts[b], (0, 255, 0), 2)
    for pt in pts:
        cv2.circle(frame, pt, 4, (0, 0, 255), -1)

# ── Camera & canvas ───────────────────────────────────────────────────────────
cap = cv2.VideoCapture(0)
canvas = np.zeros((480, 640, 3), np.uint8)
last_point = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_h, frame_w, _ = frame.shape
    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    result = detector.detect(mp_image)

    gesture = ''
    num_fingers = 0

    if result.hand_landmarks:
        hand = result.hand_landmarks[0]

        # Draw skeleton
        draw_landmarks(frame, hand, frame_w, frame_h)

        # Pixel coords
        landmarks = [(int(lm.x * frame_w), int(lm.y * frame_h)) for lm in hand]

        # ── Finger counting ───────────────────────────────────────────────
        if landmarks[4][0] < landmarks[3][0]:   # Thumb
            num_fingers += 1
        if landmarks[8][1] < landmarks[6][1]:   # Index
            num_fingers += 1
        if landmarks[12][1] < landmarks[10][1]: # Middle
            num_fingers += 1
        if landmarks[16][1] < landmarks[14][1]: # Ring
            num_fingers += 1
        if landmarks[20][1] < landmarks[18][1]: # Pinky
            num_fingers += 1

        # ── Gesture mapping ───────────────────────────────────────────────
        if num_fingers == 1:
            gesture = 'Draw Line'
        elif num_fingers == 2:
            gesture = 'Draw Rectangle'
        elif num_fingers == 3:
            gesture = 'Draw Circle'
        elif num_fingers in (4, 5):
            gesture = 'Eraser'

        # ── Drawing on canvas ─────────────────────────────────────────────
        if gesture == 'Draw Line':
            current_point = landmarks[0]
            if last_point is not None:
                cv2.line(canvas, last_point, current_point, (157, 252, 220), 2)
            last_point = current_point
        elif gesture == 'Draw Rectangle':
            cv2.rectangle(canvas, landmarks[0], landmarks[1], (200, 180, 233), 2)
            last_point = None
        elif gesture == 'Draw Circle':
            cv2.circle(canvas, landmarks[0], 50, (223, 178, 200), -1)
            last_point = None
        elif gesture == 'Eraser':
            cv2.circle(canvas, landmarks[0], 50, (0, 0, 0), -1)
            last_point = None

        cv2.imshow("Board", canvas)
    else:
        last_point = None

    # ── Overlay text ──────────────────────────────────────────────────────────
    cv2.putText(frame, gesture, (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, f"Number of Fingers: {num_fingers}", (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow("Sidra Shaikh", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()