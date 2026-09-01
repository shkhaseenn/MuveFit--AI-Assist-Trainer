import cv2
import mediapipe as mp
import math
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# ============================================================
# MOVECARE AI - BURPEE TEST
# Rep = down -> plank/floor -> upright -> jump + BOTH hands up
# ============================================================

MODEL_PATH = "pose_landmarker_full.task"
CAMERA_INDEX = 0
WIDTH = 1280
HEIGHT = 720

print("Loading MoveCare AI...")

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)

options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_poses=1,
    min_pose_detection_confidence=0.5,
    min_pose_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

detector = vision.PoseLandmarker.create_from_options(options)

print("MediaPipe ready.")

cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("ERROR: Could not open camera.")
    detector.close()
    raise SystemExit

cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

WINDOW = "MoveCare AI - Burpee Test"

cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WINDOW, WIDTH, HEIGHT)

GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)
ORANGE = (0, 165, 255)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLUE = (255, 0, 0)

# ------------------------------------------------------------
# State machine
# ------------------------------------------------------------
phase = "STANDING"
reps = 0

down_frames = 0
floor_frames = 0
return_frames = 0
jump_frames = 0

FRAMES_REQUIRED = 5
REP_COOLDOWN = 0.8
last_rep_time = 0.0

# ------------------------------------------------------------
# Report data
# ------------------------------------------------------------
session_start = time.time()
rep_scores = []

timestamp = 0


# ============================================================
# SKELETON
# ============================================================

connections = [
    (11, 12),
    (11, 13), (13, 15),
    (12, 14), (14, 16),
    (11, 23), (12, 24),
    (23, 24),
    (23, 25), (25, 27),
    (24, 26), (26, 28),
    (27, 29), (29, 31),
    (28, 30), (30, 32)
]


# ============================================================
# MAIN LOOP
# ============================================================

print("")
print("============================================")
print("       MOVECARE AI - BURPEE TEST")
print("============================================")
print("Complete burpee:")
print("DOWN -> FLOOR -> UP -> JUMP + BOTH HANDS UP")
print("Press Q to finish.")
print("")

while True:

    success, frame = cap.read()

    if not success:
        print("ERROR: Could not read camera.")
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (WIDTH, HEIGHT))

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = detector.detect_for_video(
        mp_image,
        timestamp
    )

    timestamp += 33

    # ========================================================
    # PERSON DETECTED
    # ========================================================

    if len(result.pose_landmarks) > 0:

        landmarks = result.pose_landmarks[0]

        def point(index):
            lm = landmarks[index]
            return (
                int(lm.x * WIDTH),
                int(lm.y * HEIGHT)
            )

        # Body points
        LS = point(11)
        RS = point(12)
        LW = point(15)
        RW = point(16)
        LH = point(23)
        RH = point(24)
        LK = point(25)
        RK = point(26)
        LA = point(27)
        RA = point(28)

        # ====================================================
        # DRAW SKELETON
        # ====================================================

        for a, b in connections:
            cv2.line(
                frame,
                point(a),
                point(b),
                BLUE,
                3
            )

        for index in [
            11, 12, 15, 16,
            23, 24, 25, 26,
            27, 28
        ]:
            cv2.circle(
                frame,
                point(index),
                7,
                GREEN,
                -1
            )

        # ====================================================
        # BODY POSITIONS
        # ====================================================

        shoulder_y = (LS[1] + RS[1]) / 2
        hip_y = (LH[1] + RH[1]) / 2
        knee_y = (LK[1] + RK[1]) / 2
        ankle_y = (LA[1] + RA[1]) / 2

        body_height = abs(ankle_y - shoulder_y)

        if body_height < 100:
            body_height = 100

        # ====================================================
        # BURPEE CONDITIONS
        # ====================================================

        # Person has gone down
        body_down = (
            hip_y > shoulder_y
            and
            knee_y > shoulder_y
        )

        # Person is sufficiently low
        low_position = (
            hip_y > shoulder_y + body_height * 0.10
        )

        # Person has returned upright
        body_upright = (
            hip_y < knee_y
            and
            abs(hip_y - shoulder_y) < body_height * 0.55
        )

        # Both hands clearly above shoulders
        hands_overhead = (
            LW[1] < LS[1] - 40
            and
            RW[1] < RS[1] - 40
        )

        # Feet/ankles are reasonably close to the floor
        # relative to the body; this helps identify the
        # low/floor part of the burpee.
        floor_position = (
            low_position
            and
            abs(LA[1] - RA[1]) < body_height * 0.35
        )

        # ====================================================
        # FORM SCORES
        # ====================================================

        plank_score = 100
        jump_score = 100

        if phase == "FLOOR":

            # Approximate body alignment in low position.
            shoulder_hip = abs(shoulder_y - hip_y)

            if shoulder_hip < body_height * 0.30:
                plank_score = 100
            elif shoulder_hip < body_height * 0.45:
                plank_score = 85
            else:
                plank_score = 70

        if phase == "JUMP":

            if hands_overhead:
                jump_score = 100
            else:
                jump_score = 60

        overall_score = int(
            plank_score * 0.5 +
            jump_score * 0.5
        )

        now = time.time()

        # ====================================================
        # STATE 1: STANDING
        # ====================================================

        if phase == "STANDING":

            floor_frames = 0
            return_frames = 0
            jump_frames = 0

            if body_down:
                down_frames += 1
            else:
                down_frames = 0

            if down_frames >= FRAMES_REQUIRED:
                phase = "DOWN"
                down_frames = 0

        # ====================================================
        # STATE 2: DOWN
        # ====================================================

        elif phase == "DOWN":

            if floor_position:
                floor_frames += 1
            else:
                floor_frames = 0

            if floor_frames >= FRAMES_REQUIRED:
                phase = "FLOOR"
                floor_frames = 0

        # ====================================================
        # STATE 3: FLOOR
        # ====================================================

        elif phase == "FLOOR":

            # Stay in FLOOR until the person starts returning.
            if floor_position:
                return_frames = 0
            else:
                return_frames += 1

            if return_frames >= FRAMES_REQUIRED:
                phase = "RETURNING"
                return_frames = 0

        # ====================================================
        # STATE 4: RETURNING
        # ====================================================

        elif phase == "RETURNING":

            if body_upright:
                jump_frames += 1
            else:
                jump_frames = 0

            if jump_frames >= FRAMES_REQUIRED:
                phase = "JUMP"
                jump_frames = 0

        # ====================================================
        # STATE 5: JUMP
        # ========================================================

        elif phase == "JUMP":

            # THE ONLY PLACE A REP CAN BE COUNTED.
            #
            # Must be upright AND both hands must be overhead.
            # The person has already completed the DOWN/FLOOR/
            # RETURNING states before reaching this state.

            if (
                body_upright
                and
                hands_overhead
                and
                now - last_rep_time >= REP_COOLDOWN
            ):

                reps += 1
                last_rep_time = now

                rep_score = int(
                    plank_score * 0.5 +
                    jump_score * 0.5
                )

                rep_scores.append(rep_score)

                print(
                    f"BURPEE REP {reps} COMPLETED - "
                    f"SCORE: {rep_score}%"
                )

                # Reset for next burpee
                phase = "STANDING"

                down_frames = 0
                floor_frames = 0
                return_frames = 0
                jump_frames = 0

        # ====================================================
        # FEEDBACK
        # ====================================================

        if phase == "STANDING":
            feedback = "READY - GO DOWN"
            feedback_color = GREEN

        elif phase == "DOWN":
            feedback = "KEEP GOING DOWN"
            feedback_color = YELLOW

        elif phase == "FLOOR":
            feedback = "FLOOR / PLANK"
            feedback_color = YELLOW

        elif phase == "RETURNING":
            feedback = "COME UP"
            feedback_color = YELLOW

        elif phase == "JUMP":

            if hands_overhead:
                feedback = "HANDS UP - REP!"
                feedback_color = GREEN
            else:
                feedback = "JUMP + BOTH HANDS UP"
                feedback_color = ORANGE

        else:
            feedback = "READY"
            feedback_color = GREEN

        # ====================================================
        # MAIN PANEL
        # ====================================================

        cv2.rectangle(
            frame,
            (15, 15),
            (520, 300),
            (0, 0, 0),
            -1
        )

        cv2.putText(
            frame,
            "MOVECARE AI",
            (35, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            YELLOW,
            2
        )

        cv2.putText(
            frame,
            "BURPEE TEST",
            (35, 82),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            WHITE,
            2
        )

        cv2.putText(
            frame,
            f"REPS: {reps}",
            (35, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            GREEN,
            3
        )

        cv2.putText(
            frame,
            f"PHASE: {phase}",
            (235, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            YELLOW,
            2
        )

        cv2.putText(
            frame,
            f"FORM: {overall_score}%",
            (35, 165),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            WHITE,
            2
        )

        cv2.putText(
            frame,
            f"PLANK: {plank_score}%",
            (35, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            GREEN if plank_score >= 80 else ORANGE,
            2
        )

        cv2.putText(
            frame,
            f"JUMP: {jump_score}%",
            (235, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            GREEN if jump_score >= 80 else ORANGE,
            2
        )

        hand_text = (
            "BOTH HANDS UP: YES"
            if hands_overhead
            else "BOTH HANDS UP: NO"
        )

        cv2.putText(
            frame,
            hand_text,
            (35, 238),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.52,
            GREEN if hands_overhead else ORANGE,
            2
        )

        cv2.putText(
            frame,
            feedback,
            (35, 275),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.52,
            feedback_color,
            2
        )

    else:

        cv2.putText(
            frame,
            "NO PERSON DETECTED",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            RED,
            3
        )

    # ========================================================
    # SHOW
    # ========================================================

    cv2.imshow(
        WINDOW,
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


# ============================================================
# FINAL REPORT
# ============================================================

session_duration = time.time() - session_start

if len(rep_scores) > 0:
    final_score = sum(rep_scores) / len(rep_scores)
    best_rep = max(rep_scores)
    worst_rep = min(rep_scores)
else:
    final_score = 0
    best_rep = 0
    worst_rep = 0

if final_score >= 90:
    rating = "EXCELLENT"
elif final_score >= 80:
    rating = "GOOD"
elif final_score >= 70:
    rating = "FAIR"
elif final_score >= 60:
    rating = "NEEDS IMPROVEMENT"
else:
    rating = "NO DATA"

print("")
print("============================================")
print("       MOVECARE AI - BURPEE REPORT")
print("============================================")
print(f"Total Burpees:       {reps}")
print(f"Duration:            {session_duration:.1f} seconds")
print(f"Average Form Score:  {final_score:.1f}%")
print(f"Best Rep:            {best_rep}%")
print(f"Worst Rep:           {worst_rep}%")
print(f"Rating:              {rating}")
print("============================================")

exercise_result = {
    "exercise": "burpee",
    "repetitions": reps,
    "duration_seconds": round(session_duration, 2),
    "overall_score": round(final_score, 1),
    "rating": rating,
    "rep_scores": rep_scores,
    "analysis": {
        "plank_score": round(plank_score, 1),
        "jump_score": round(jump_score, 1),
        "both_hands_overhead_required": True
    }
}

print("")
print("MOVECARE AI RESULT:")
print(exercise_result)

cap.release()
cv2.destroyAllWindows()
detector.close()
