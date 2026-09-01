import cv2
import mediapipe as mp

# MediaPipe Tasks API
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# Downloaded model will go here
MODEL_PATH = "pose_landmarker_full.task"


# Create Pose Landmarker
base_options = python.BaseOptions(
    model_asset_path=MODEL_PATH
)

options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_poses=1,
    min_pose_detection_confidence=0.5,
    min_pose_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

detector = vision.PoseLandmarker.create_from_options(options)


# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open webcam.")
    exit()

print("Webcam started.")
print("Press Q to quit.")

frame_timestamp_ms = 0

while True:

    success, frame = cap.read()

    if not success:
        print("ERROR: Could not read webcam frame.")
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    # Convert BGR -> RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert to MediaPipe image
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    # Detect pose
    result = detector.detect_for_video(
        mp_image,
        frame_timestamp_ms
    )

    frame_timestamp_ms += 33

    # Draw landmarks
    if result.pose_landmarks:

        landmarks = result.pose_landmarks[0]

        h, w, _ = frame.shape

        # Draw the 33 points
        for i, landmark in enumerate(landmarks):

            x = int(landmark.x * w)
            y = int(landmark.y * h)

            # Green point
            cv2.circle(
                frame,
                (x, y),
                5,
                (0, 255, 0),
                -1
            )

            # Point number
            cv2.putText(
                frame,
                str(i),
                (x + 6, y - 6),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (0, 255, 255),
                1
            )

        # Draw connections
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 7),
            (0, 4), (4, 5), (5, 6), (6, 8),

            (9, 10),

            (11, 12),

            (11, 13),
            (13, 15),

            (12, 14),
            (14, 16),

            (11, 23),
            (12, 24),

            (23, 24),

            (23, 25),
            (25, 27),
            (27, 29),
            (29, 31),

            (24, 26),
            (26, 28),
            (28, 30),
            (30, 32),

            (27, 28)
        ]

        for a, b in connections:

            x1 = int(landmarks[a].x * w)
            y1 = int(landmarks[a].y * h)

            x2 = int(landmarks[b].x * w)
            y2 = int(landmarks[b].y * h)

            cv2.line(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2
            )

        # Show number of detected points
        cv2.putText(
            frame,
            "33-POINT POSE TRACKING",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    else:

        cv2.putText(
            frame,
            "NO PERSON DETECTED",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    cv2.imshow(
        "MoveCare AI - Body Tracking Test",
        frame
    )

    # Q = quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
detector.close()
