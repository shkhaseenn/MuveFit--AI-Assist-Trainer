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

# Alignment thresholds for a valid Glute Bridge (Shoulder-Hip-Knee angle)
BRIDGE_HIP_ANGLE_MIN = 155.0   # Minimum angle to ensure hips are fully extended
BRIDGE_HIP_ANGLE_MAX = 195.0   # Maximum angle to prevent lumbar hyperextension
TORSO_ON_FLOOR_MAX = 0.35      # Ensures user is lying down near floor level
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

WINDOW = "MoveCare AI - Glute Bridge Hold"

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
# GLUTE BRIDGE STATE
# ============================================================

is_holding = False
hold_start_time = 0
total_hold_time = 0.0
hold_status = "LIE ON BACK & BEND KNEES"

hold_frames = 0
stand_frames = 0


# ============================================================
# START
# ============================================================

print("")
print("============================================")
print("     MOVECARE AI - GLUTE BRIDGE HOLD")
print("============================================")
print("")
print("Lie down on your back SIDEWAYS to the camera.")
print("Bend knees, feet flat, drive hips up into a straight line.")
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
        # KEY POINTS FOR GLUTE BRIDGE
        # ====================================================

        LS = point(11)  # Left Shoulder
        RS = point(12)  # Right Shoulder
        LH = point(23)  # Left Hip
        RH = point(24)  # Right Hip
        LK = point(25)  # Left Knee
        RK = point(26)  # Right Knee

        LS_n = point_norm(11)
        RS_n = point_norm(12)

        # ====================================================
        # METRICS & ANGLE CALCULATIONS
        # ====================================================

        # Shoulder-Hip-Knee angle measures hip extension
        left_hip_angle = calculate_angle(LS, LH, LK)
        right_hip_angle = calculate_angle(RS, RH, RK)

        avg_hip_angle = (left_hip_angle + right_hip_angle) / 2.0

        # Height check to ensure user is down near floor level
        avg_shoulder_y = (LS_n[1] + RS_n[1]) / 2.0

        # Draw live angle directly next to hips
        cv2.putText(frame, f"{int(avg_hip_angle)} deg", (LH[0] + 10, LH[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # ====================================================
        # GLUTE BRIDGE HOLD LOGIC
        # ====================================================

        is_extended = BRIDGE_HIP_ANGLE_MIN <= avg_hip_angle <= BRIDGE_HIP_ANGLE_MAX
        is_on_ground = avg_shoulder_y >= TORSO_ON_FLOOR_MAX

        if is_extended and is_on_ground:
            hold_frames += 1
            stand_frames = 0

            if hold_frames >= FRAMES_REQUIRED:
                if not is_holding:
                    is_holding = True
                    hold_start_time = current_time - total_hold_time
                
                hold_status = "HOLDING BRIDGE"
                total_hold_time = current_time - hold_start_time

        else:
            stand_frames += 1
            hold_frames = 0

            if stand_frames >= FRAMES_REQUIRED:
                is_holding = False
                
                if not is_on_ground:
                    hold_status = "LIE DOWN ON FLOOR"
                elif avg_hip_angle < BRIDGE_HIP_ANGLE_MIN:
                    hold_status = "LIFT HIPS HIGHER"
                else:
                    hold_status = "TOO HIGH (LOWER HIPS)"

        # ====================================================
        # INFORMATION PANEL
        # ====================================================

        panel_color = (0, 180, 0) if is_holding else (0, 0, 0)

        cv2.rectangle(
            frame,
            (10, 10),
            (430, 210),
            panel_color,
            -1
        )

        cv2.putText(
            frame,
            f"BRIDGE TIME: {total_hold_time:.1f}s",
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
            f"Hip Angle:  {avg_hip_angle:.1f} deg",
            (25, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Left Hip:   {left_hip_angle:.1f} deg",
            (25, 155),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (200, 200, 200),
            1
        )

        cv2.putText(
            frame,
            f"Right Hip:  {right_hip_angle:.1f} deg",
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
print(f"Tracking stopped. Total Glute Bridge Hold Time: {total_hold_time:.1f} seconds.")