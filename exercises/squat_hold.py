import cv2
import mediapipe as mp
import math
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# ============================================================
# SETTINGS
# ============================================================

MODEL_PATH = "pose_landmarker_full.task"

CAMERA_INDEX = 0

WIDTH = 1280
HEIGHT = 720

# Adjusted thresholds: standard parallel squat knee angle is ~90 degrees
SQUAT_KNEE_ANGLE_MAX = 115.0  # Upper limit to enter/maintain squat hold
SQUAT_KNEE_ANGLE_MIN = 50.0   # Lower limit to prevent collapsing
FRAMES_REQUIRED = 3           # Debounce threshold to prevent flickering


# ============================================================
# ANGLE CALCULATION (ROBUST VECTOR MATH)
# ============================================================

def calculate_angle(a, b, c):
    """
    Calculates the 2D angle (in degrees) at vertex point b between points a and c.
    Returns 180 when straight, ~90 when bent at a right angle.
    """
    ba = (a[0] - b[0], a[1] - b[1])
    bc = (c[0] - b[0], c[1] - b[1])

    dot_product = ba[0] * bc[0] + ba[1] * bc[1]
    magnitude_ba = math.hypot(ba[0], ba[1])
    magnitude_bc = math.hypot(bc[0], bc[1])

    if magnitude_ba * magnitude_bc == 0:
        return 180.0

    cos_angle = dot_product / (magnitude_ba * magnitude_bc)
    cos_angle = max(-1.0, min(1.0, cos_angle))  # Clamp to handle float precision issues

    return math.degrees(math.acos(cos_angle))


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

WINDOW = "MoveCare AI - Squat Hold"

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
# SQUAT HOLD STATE
# ============================================================

is_holding = False
hold_start_time = 0
total_hold_time = 0.0
hold_status = "STAND UP"

hold_frames = 0
stand_frames = 0


# ============================================================
# START
# ============================================================

print("")
print("============================================")
print("        MOVECARE AI - SQUAT HOLD")
print("============================================")
print("")
print("Stand SIDEWAYS to camera where FULL BODY is visible.")
print("Squat down until knee angle is between 50 and 115 degrees.")
print("Press F to toggle Fullscreen.")
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

    # Mirror camera horizontally
    frame = cv2.flip(
        frame,
        1
    )

    current_time = time.time()

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

            x = int(lm.x * width)
            y = int(lm.y * height)

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
        # KEY POINTS FOR ANGLES
        # ====================================================

        LH = point(23)  # Left Hip
        RH = point(24)  # Right Hip

        LK = point(25)  # Left Knee
        RK = point(26)  # Right Knee

        LA = point(27)  # Left Ankle
        RA = point(28)  # Right Ankle

        # ====================================================
        # ANGLE CALCULATIONS
        # ====================================================

        left_knee = calculate_angle(LH, LK, LA)
        right_knee = calculate_angle(RH, RK, RA)

        # Primary knee angle (uses minimum visible bent angle)
        avg_knee = (left_knee + right_knee) / 2.0

        # Draw live angle directly next to knees on video
        cv2.putText(frame, f"{int(left_knee)} deg", (LK[0] + 10, LK[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"{int(right_knee)} deg", (RK[0] + 10, RK[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # ====================================================
        # SQUAT HOLD LOGIC
        # ====================================================

        in_squat_range = SQUAT_KNEE_ANGLE_MIN <= avg_knee <= SQUAT_KNEE_ANGLE_MAX

        if in_squat_range:
            hold_frames += 1
            stand_frames = 0

            if hold_frames >= FRAMES_REQUIRED:
                if not is_holding:
                    is_holding = True
                    hold_start_time = current_time - total_hold_time  # Resume timer if paused
                
                hold_status = "HOLDING"
                total_hold_time = current_time - hold_start_time

        else:
            stand_frames += 1
            hold_frames = 0

            if stand_frames >= FRAMES_REQUIRED:
                is_holding = False
                
                if avg_knee > SQUAT_KNEE_ANGLE_MAX:
                    hold_status = "SQUAT LOWER"
                else:
                    hold_status = "TOO DEEP"

        # ====================================================
        # INFORMATION PANEL
        # ====================================================

        panel_color = (0, 180, 0) if is_holding else (0, 0, 0)

        cv2.rectangle(
            frame,
            (10, 10),
            (390, 210),
            panel_color,
            -1
        )

        cv2.putText(
            frame,
            f"HOLD TIME: {total_hold_time:.1f}s",
            (25, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 0) if is_holding else (0, 255, 255),
            3
        )

        cv2.putText(
            frame,
            f"Status:     {hold_status}",
            (25, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Avg Knee:   {avg_knee:.1f} deg",
            (25, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Left Knee:  {left_knee:.1f} deg",
            (25, 155),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (200, 200, 200),
            1
        )

        cv2.putText(
            frame,
            f"Right Knee: {right_knee:.1f} deg",
            (25, 185),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (200, 200, 200),
            1
        )

    # ========================================================
    # NO PERSON
    # ========================================================

    else:
        is_holding = False
        hold_frames = 0

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
    # KEYBOARD CONTROLS
    # ========================================================

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    elif key == ord("f"):
        prop = cv2.getWindowProperty(WINDOW, cv2.WND_PROP_FULLSCREEN)
        if prop == cv2.WINDOW_FULLSCREEN:
            cv2.setWindowProperty(WINDOW, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
        else:
            cv2.setWindowProperty(WINDOW, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


# ============================================================
# CLEANUP
# ============================================================

cap.release()
cv2.destroyAllWindows()
detector.close()

print("")
print(f"Tracking stopped. Total Squat Hold Time: {total_hold_time:.1f} seconds.")