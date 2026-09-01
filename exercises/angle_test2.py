import cv2
import mediapipe as mp
import math

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# ============================================================
# SETTINGS
# ============================================================

MODEL_PATH = "pose_landmarker_full.task"

CAMERA_INDEX = 0

WIDTH = 1280
HEIGHT = 720


# ============================================================
# ANGLE CALCULATION
# ============================================================

def calculate_angle(a, b, c):

    angle = math.degrees(
        math.atan2(c[1] - b[1], c[0] - b[0])
        -
        math.atan2(a[1] - b[1], a[0] - b[0])
    )

    angle = abs(angle)

    if angle > 180:
        angle = 360 - angle

    return angle


# ============================================================
# MEDIAPIPE
# ============================================================

base_options = python.BaseOptions(
    model_asset_path=MODEL_PATH
)

options = vision.PoseLandmarkerOptions(
    base_options=base_options,

    running_mode=vision.RunningMode.VIDEO,

    num_poses=1,

    min_pose_detection_confidence=0.3,
    min_pose_presence_confidence=0.3,
    min_tracking_confidence=0.3
)

detector = vision.PoseLandmarker.create_from_options(
    options
)


# ============================================================
# CAMERA
# ============================================================

cap = cv2.VideoCapture(
    CAMERA_INDEX,
    cv2.CAP_DSHOW
)

if not cap.isOpened():

    print("ERROR: Camera could not be opened.")

    exit()


cap.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    WIDTH
)

cap.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    HEIGHT
)

cap.set(
    cv2.CAP_PROP_BUFFERSIZE,
    1
)


actual_width = int(
    cap.get(cv2.CAP_PROP_FRAME_WIDTH)
)

actual_height = int(
    cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
)

print(
    f"Camera resolution: "
    f"{actual_width} x {actual_height}"
)


# ============================================================
# WINDOW
# ============================================================

WINDOW = "MoveCare AI - Angle Test 2"

cv2.namedWindow(
    WINDOW,
    cv2.WINDOW_NORMAL
)

cv2.resizeWindow(
    WINDOW,
    1280,
    720
)


# ============================================================
# BODY CONNECTIONS
# ============================================================

connections = [

    # Head
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 7),

    (0, 4),
    (4, 5),
    (5, 6),
    (6, 8),

    (9, 10),

    # Shoulders
    (11, 12),

    # Left arm
    (11, 13),
    (13, 15),

    # Right arm
    (12, 14),
    (14, 16),

    # Torso
    (11, 23),
    (12, 24),

    # Hips
    (23, 24),

    # Left leg
    (23, 25),
    (25, 27),

    # Right leg
    (24, 26),
    (26, 28),

    # Feet
    (27, 29),
    (29, 31),

    (28, 30),
    (30, 32),

    # Ankles
    (27, 28)
]


# ============================================================
# START
# ============================================================

print("")
print("============================================")
print("       MOVECARE AI - ANGLE TEST 2")
print("============================================")
print("")
print("Stand where your FULL BODY is visible.")
print("Press Q to quit.")
print("")


timestamp = 0


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    success, frame = cap.read()

    if not success:

        print("Could not read camera frame.")

        break


    # Mirror camera
    frame = cv2.flip(
        frame,
        1
    )


    # --------------------------------------------------------
    # RGB
    # --------------------------------------------------------

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    # --------------------------------------------------------
    # MediaPipe image
    # --------------------------------------------------------

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )


    # --------------------------------------------------------
    # Detect
    # --------------------------------------------------------

    result = detector.detect_for_video(
        mp_image,
        timestamp
    )

    timestamp += 33


    height, width, _ = frame.shape


    # ========================================================
    # PERSON FOUND
    # ========================================================

    if len(result.pose_landmarks) > 0:

        landmarks = result.pose_landmarks[0]


        print(
            "PERSON DETECTED",
            end="\r"
        )


        # ----------------------------------------------------
        # Point converter
        # ----------------------------------------------------

        def point(index):

            lm = landmarks[index]

            return (
                int(lm.x * width),
                int(lm.y * height)
            )


        # ----------------------------------------------------
        # Draw connections
        # ----------------------------------------------------

        for a, b in connections:

            p1 = point(a)
            p2 = point(b)

            cv2.line(
                frame,
                p1,
                p2,
                (255, 0, 0),
                3
            )


        # ----------------------------------------------------
        # Draw ALL 33 points
        # ----------------------------------------------------

        for i in range(33):

            lm = landmarks[i]

            x = int(
                lm.x * width
            )

            y = int(
                lm.y * height
            )


            cv2.circle(
                frame,
                (x, y),
                6,
                (0, 255, 0),
                -1
            )


            cv2.putText(
                frame,
                str(i),
                (x + 7, y - 7),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.45,

                (0, 255, 255),

                1
            )


        # ====================================================
        # IMPORTANT POINTS
        # ====================================================

        LS = point(11)
        RS = point(12)

        LH = point(23)
        RH = point(24)

        LK = point(25)
        RK = point(26)

        LA = point(27)
        RA = point(28)


        # ====================================================
        # KNEE ANGLES
        # ====================================================

        left_knee = calculate_angle(
            LH,
            LK,
            LA
        )

        right_knee = calculate_angle(
            RH,
            RK,
            RA
        )


        # ====================================================
        # HIP ANGLES
        # ====================================================

        left_hip = calculate_angle(
            LS,
            LH,
            LK
        )

        right_hip = calculate_angle(
            RS,
            RH,
            RK
        )


        # ====================================================
        # INFORMATION PANEL
        # ====================================================

        cv2.rectangle(
            frame,

            (10, 10),

            (390, 190),

            (0, 0, 0),

            -1
        )


        cv2.putText(
            frame,

            "PERSON DETECTED",

            (25, 42),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (0, 255, 0),

            2
        )


        cv2.putText(
            frame,

            f"Left Knee:  {left_knee:.1f}",

            (25, 78),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.65,

            (0, 255, 255),

            2
        )


        cv2.putText(
            frame,

            f"Right Knee: {right_knee:.1f}",

            (25, 110),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.65,

            (0, 255, 255),

            2
        )


        cv2.putText(
            frame,

            f"Left Hip:   {left_hip:.1f}",

            (25, 142),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.65,

            (255, 255, 0),

            2
        )


        cv2.putText(
            frame,

            f"Right Hip:  {right_hip:.1f}",

            (25, 174),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.65,

            (255, 255, 0),

            2
        )


    # ========================================================
    # NO PERSON
    # ========================================================

    else:

        cv2.putText(
            frame,

            "NO PERSON DETECTED",

            (30, 50),

            cv2.FONT_HERSHEY_SIMPLEX,

            1.0,

            (0, 0, 255),

            3
        )


    # ========================================================
    # SHOW
    # ========================================================

    cv2.imshow(
        WINDOW,
        frame
    )


    # ========================================================
    # QUIT
    # ========================================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# ============================================================
# CLEANUP
# ============================================================

cap.release()

cv2.destroyAllWindows()

detector.close()

print("")
print("Tracking stopped.")
