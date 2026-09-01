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

# Alignment thresholds for a valid plank
PLANK_BODY_ANGLE_MIN = 150.0   # Shoulder-Hip-Ankle body line (180 = flat line)
PLANK_BODY_ANGLE_MAX = 195.0   # Max angle to prevent sagging or arching
PLANK_TORSO_HORIZONTAL_MAX = 0.20  # Max height delta (Y-axis) between shoulders and hips
FRAMES_REQUIRED = 3            # Debounce threshold to prevent flickering


# ============================================================
# ANGLE CALCULATION (ROBUST VECTOR MATH)
# ============================================================

def calculate_angle(a, b, c):
    """
    Calculates the 2D angle (in degrees) at vertex point b between points a and c.
    Returns 180 when straight, <180 when bent.
    """
    ba = (a[0] - b[0], a[1] - b[1])
    bc = (c[0] - b[0], c[1] - b[1])

    dot_product = ba[0] * bc[0] + ba[1] * bc[1]
    magnitude_ba = math.hypot(ba[0], ba[1])
    magnitude_bc = math.hypot(bc[0], bc[1])

    if magnitude_ba * magnitude_bc == 0:
        return 180.0

    cos_angle = dot_product / (magnitude_ba * magnitude_bc)
    cos_angle = max(-1.0, min(1.0, cos_angle))

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

WINDOW = "MoveCare AI - Plank Hold"

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
# PLANK HOLD STATE
# ============================================================

is_holding = False
hold_start_time = 0
total_hold_time = 0.0
hold_status = "GET INTO PLANK"

hold_frames = 0
stand_frames = 0


# ============================================================
# START
# ============================================================

print("")
print("============================================")
print("        MOVECARE AI - PLANK HOLD")
print("============================================")
print("")
print("Get down on the floor facing SIDEWAYS to the camera.")
print("Keep your body straight from shoulders to ankles.")
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
        # Point converters
        # ----------------------------------------------------

        def point(index):
            lm = landmarks[index]
            return (
                int(lm.x * width),
                int(lm.y * height)
            )

        def point_norm(index):
            lm = landmarks[index]
            return (lm.x, lm.y)

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
        # KEY POINTS FOR PLANK
        # ====================================================

        LS = point(11)  # Left Shoulder
        RS = point(12)  # Right Shoulder
        LH = point(23)  # Left Hip
        RH = point(24)  # Right Hip
        LA = point(27)  # Left Ankle
        RA = point(28)  # Right Ankle

        LS_n = point_norm(11)
        RS_n = point_norm(12)
        LH_n = point_norm(23)
        RH_n = point_norm(24)

        # ====================================================
        # METRICS & ANGLE CALCULATIONS
        # ====================================================

        left_body = calculate_angle(LS, LH, LA)
        right_body = calculate_angle(RS, RH, RA)

        avg_body_angle = (left_body + right_body) / 2.0

        # Height difference between shoulder and hip normalized (determines if horizontal)
        avg_shoulder_y = (LS_n[1] + RS_n[1]) / 2.0
        avg_hip_y = (LH_n[1] + RH_n[1]) / 2.0
        torso_height_diff = abs(avg_shoulder_y - avg_hip_y)

        # Draw live angle directly next to hips
        cv2.putText(frame, f"{int(avg_body_angle)} deg", (LH[0] + 10, LH[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # ====================================================
        # PLANK HOLD LOGIC
        # ====================================================

        is_straight_line = PLANK_BODY_ANGLE_MIN <= avg_body_angle <= PLANK_BODY_ANGLE_MAX
        is_horizontal = torso_height_diff <= PLANK_TORSO_HORIZONTAL_MAX

        if is_straight_line and is_horizontal:
            hold_frames += 1
            stand_frames = 0

            if hold_frames >= FRAMES_REQUIRED:
                if not is_holding:
                    is_holding = True
                    hold_start_time = current_time - total_hold_time
                
                hold_status = "HOLDING PLANK"
                total_hold_time = current_time - hold_start_time

        else:
            stand_frames += 1
            hold_frames = 0

            if stand_frames >= FRAMES_REQUIRED:
                is_holding = False
                
                if not is_horizontal:
                    hold_status = "GET DOWN TO FLOOR"
                elif avg_body_angle < PLANK_BODY_ANGLE_MIN:
                    if avg_hip_y > avg_shoulder_y:
                        hold_status = "HIPS SAGGING (LIFT UP)"
                    else:
                        hold_status = "HIPS TOO HIGH (LOWER DOWN)"
                else:
                    hold_status = "ALIGN YOUR BODY"

        # ====================================================
        # INFORMATION PANEL
        # ====================================================

        panel_color = (0, 180, 0) if is_holding else (0, 0, 0)

        cv2.rectangle(
            frame,
            (10, 10),
            (420, 210),
            panel_color,
            -1
        )

        cv2.putText(
            frame,
            f"PLANK TIME: {total_hold_time:.1f}s",
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
            0.6,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Body Line:  {avg_body_angle:.1f} deg",
            (25, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Left Body:  {left_body:.1f} deg",
            (25, 155),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (200, 200, 200),
            1
        )

        cv2.putText(
            frame,
            f"Right Body: {right_body:.1f} deg",
            (25, 185),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
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
print(f"Tracking stopped. Total Plank Hold Time: {total_hold_time:.1f} seconds.")