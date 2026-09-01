import cv2
import mediapipe as mp
import math
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# ============================================================
# MOVECARE AI — SQUAT TEST
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
# LANDMARK → POINT
# ============================================================

def landmark_to_point(landmark):

    return (
        landmark.x,
        landmark.y
    )


# ============================================================
# MEDIAPIPE
# ============================================================

print("Loading MoveCare AI...")

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

detector = vision.PoseLandmarker.create_from_options(
    options
)

print("MediaPipe ready.")


# ============================================================
# CAMERA
# ============================================================

cap = cv2.VideoCapture(
    CAMERA_INDEX,
    cv2.CAP_DSHOW
)

if not cap.isOpened():

    print("ERROR: Could not open camera.")

    detector.close()

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


# ============================================================
# WINDOW
# ============================================================

WINDOW = "MoveCare AI - Squat Test"

cv2.namedWindow(
    WINDOW,
    cv2.WINDOW_NORMAL
)

cv2.resizeWindow(
    WINDOW,
    WIDTH,
    HEIGHT
)


# ============================================================
# SQUAT SETTINGS
# ============================================================

DEEP_SQUAT_ANGLE = 100

STANDING_ANGLE = 165


# ============================================================
# STABILITY
# ============================================================

DOWN_FRAMES_REQUIRED = 8

UP_FRAMES_REQUIRED = 8


down_frames = 0

up_frames = 0


# ============================================================
# REP COOLDOWN
# ============================================================

REP_COOLDOWN = 1.0

last_rep_time = 0


# ============================================================
# STATE
# ============================================================

reps = 0

stage = "UP"


# ============================================================
# SCORES
# ============================================================

depth_score = 100

knee_score = 100

torso_score = 100

overall_score = 100


# ============================================================
# STATISTICS
# ============================================================

depth_good_frames = 0

depth_bad_frames = 0

knee_good_frames = 0

knee_bad_frames = 0

torso_good_frames = 0

torso_bad_frames = 0


# ============================================================
# ISSUES
# ============================================================

shallow_squat_frames = 0

knee_alignment_frames = 0

torso_lean_frames = 0


# ============================================================
# DEPTH
# ============================================================

lowest_knee_angle = 180


# ============================================================
# SESSION
# ============================================================

session_start = time.time()


# ============================================================
# SKELETON CONNECTIONS
# ============================================================

connections = [

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

    (24, 26),
    (26, 28),

    (27, 29),
    (29, 31),

    (28, 30),
    (30, 32)
]


# ============================================================
# START
# ============================================================

print("")
print("==========================================")
print("        MOVECARE AI - SQUAT TEST")
print("==========================================")
print("")
print("Both knees must reach <= 100 degrees.")
print("Then return to >= 165 degrees.")
print("")
print("Press Q to finish.")
print("")


# ============================================================
# TIMESTAMP
# ============================================================

frame_timestamp = 0


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    ret, frame = cap.read()

    if not ret:

        print("ERROR: Could not read camera.")

        break


    # --------------------------------------------------------
    # MIRROR CAMERA
    # --------------------------------------------------------

    frame = cv2.flip(
        frame,
        1
    )


    # --------------------------------------------------------
    # RESIZE
    # --------------------------------------------------------

    frame = cv2.resize(
        frame,
        (WIDTH, HEIGHT)
    )


    # --------------------------------------------------------
    # RGB
    # --------------------------------------------------------

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )


    # --------------------------------------------------------
    # TIMESTAMP
    # --------------------------------------------------------

    frame_timestamp += 33


    # --------------------------------------------------------
    # POSE
    # --------------------------------------------------------

    result = detector.detect_for_video(
        mp_image,
        frame_timestamp
    )


    # ========================================================
    # PERSON FOUND
    # ========================================================

    if result.pose_landmarks:

        landmarks = result.pose_landmarks[0]


        # ====================================================
        # GET LANDMARKS
        # ====================================================

        left_shoulder = landmark_to_point(
            landmarks[11]
        )

        right_shoulder = landmark_to_point(
            landmarks[12]
        )

        left_hip = landmark_to_point(
            landmarks[23]
        )

        right_hip = landmark_to_point(
            landmarks[24]
        )

        left_knee = landmark_to_point(
            landmarks[25]
        )

        right_knee = landmark_to_point(
            landmarks[26]
        )

        left_ankle = landmark_to_point(
            landmarks[27]
        )

        right_ankle = landmark_to_point(
            landmarks[28]
        )


        # ====================================================
        # PIXEL COORDINATES
        # ====================================================

        def pixel_point(point):

            return (

                int(point[0] * WIDTH),

                int(point[1] * HEIGHT)

            )


        ls = pixel_point(left_shoulder)
        rs = pixel_point(right_shoulder)

        lh = pixel_point(left_hip)
        rh = pixel_point(right_hip)

        lk = pixel_point(left_knee)
        rk = pixel_point(right_knee)

        la = pixel_point(left_ankle)
        ra = pixel_point(right_ankle)


        # ====================================================
        # DRAW SKELETON
        # ====================================================

        for start, end in connections:

            p1 = landmarks[start]

            p2 = landmarks[end]

            x1 = int(p1.x * WIDTH)
            y1 = int(p1.y * HEIGHT)

            x2 = int(p2.x * WIDTH)
            y2 = int(p2.y * HEIGHT)

            cv2.line(

                frame,

                (x1, y1),

                (x2, y2),

                (255, 255, 255),

                2
            )


        # ====================================================
        # DRAW JOINTS
        # ====================================================

        points = [

            ls,
            rs,

            lh,
            rh,

            lk,
            rk,

            la,
            ra
        ]

        for p in points:

            cv2.circle(

                frame,

                p,

                6,

                (0, 255, 0),

                -1
            )


        # ====================================================
        # KNEE ANGLES
        # ====================================================

        left_knee_angle = calculate_angle(

            left_hip,
            left_knee,
            left_ankle
        )

        right_knee_angle = calculate_angle(

            right_hip,
            right_knee,
            right_ankle
        )


        current_knee_angle = (

            left_knee_angle +
            right_knee_angle

        ) / 2


        # ====================================================
        # LOWEST DEPTH
        # ====================================================

        if current_knee_angle < lowest_knee_angle:

            lowest_knee_angle = current_knee_angle


        # ====================================================
        # TORSO ANGLES
        # ====================================================

        left_torso_angle = calculate_angle(

            left_shoulder,
            left_hip,
            left_knee
        )

        right_torso_angle = calculate_angle(

            right_shoulder,
            right_hip,
            right_knee
        )


        torso_angle = (

            left_torso_angle +
            right_torso_angle

        ) / 2


        # ====================================================
        # FORM SCORES FOR CURRENT FRAME
        # ====================================================

        current_depth_score = 100

        current_knee_score = 100

        current_torso_score = 100

        feedback = "GOOD FORM"


        # ====================================================
        # ONLY SCORE DEPTH DURING SQUAT
        # ====================================================

        if current_knee_angle < 160:

            if current_knee_angle <= 100:

                current_depth_score = 100

                depth_good_frames += 1


            elif current_knee_angle <= 120:

                current_depth_score = 75

                depth_bad_frames += 1

                shallow_squat_frames += 1

                feedback = "GO DEEPER"


            elif current_knee_angle <= 145:

                current_depth_score = 55

                depth_bad_frames += 1

                shallow_squat_frames += 1

                feedback = "SQUAT LOWER"


            else:

                current_depth_score = 40

                depth_bad_frames += 1

                shallow_squat_frames += 1

                feedback = "BEND YOUR KNEES"


        else:

            # Standing / transition.
            current_depth_score = 100


        # ====================================================
        # KNEE ALIGNMENT
        # ====================================================

        knee_difference = abs(

            left_knee_angle -
            right_knee_angle

        )


        if knee_difference <= 10:

            current_knee_score = 100

            knee_good_frames += 1


        elif knee_difference <= 20:

            current_knee_score = 75

            knee_bad_frames += 1

            knee_alignment_frames += 1

            feedback = "CHECK KNEE ALIGNMENT"


        else:

            current_knee_score = 50

            knee_bad_frames += 1

            knee_alignment_frames += 1

            feedback = "KNEES NOT ALIGNED"


        # ====================================================
        # TORSO
        # ====================================================

        if current_knee_angle < 160:

            if torso_angle >= 155:

                current_torso_score = 100

                torso_good_frames += 1


            elif torso_angle >= 135:

                current_torso_score = 75

                torso_bad_frames += 1

                torso_lean_frames += 1

                feedback = "KEEP CHEST UP"


            else:

                current_torso_score = 50

                torso_bad_frames += 1

                torso_lean_frames += 1

                feedback = "REDUCE FORWARD LEAN"


        else:

            current_torso_score = 100


        # ====================================================
        # OVERALL FRAME SCORE
        # ====================================================

        current_frame_score = (

            current_depth_score * 0.40 +

            current_knee_score * 0.35 +

            current_torso_score * 0.25

        )


        # ====================================================
        # REP DETECTION
        # ====================================================

        current_time = time.time()


        # ----------------------------------------------------
        # GOING DOWN
        # ----------------------------------------------------

        if current_knee_angle <= DEEP_SQUAT_ANGLE:

            down_frames += 1

            up_frames = 0

            if (

                down_frames >= DOWN_FRAMES_REQUIRED

                and

                stage == "UP"

            ):

                stage = "DOWN"


        # ----------------------------------------------------
        # RETURNING UP
        # ----------------------------------------------------

        elif current_knee_angle >= STANDING_ANGLE:

            up_frames += 1

            down_frames = 0


            if (

                up_frames >= UP_FRAMES_REQUIRED

                and

                stage == "DOWN"

                and

                current_time - last_rep_time >= REP_COOLDOWN

            ):

                reps += 1

                last_rep_time = current_time

                stage = "UP"

                print(
                    f"Squat rep completed: {reps}"
                )


        # ----------------------------------------------------
        # TRANSITION
        # ----------------------------------------------------

        else:

            down_frames = 0

            up_frames = 0


        # ====================================================
        # RUNNING SCORES
        # ====================================================

        depth_score = current_depth_score

        knee_score = current_knee_score

        torso_score = current_torso_score


        overall_score = (

            depth_score * 0.40 +

            knee_score * 0.35 +

            torso_score * 0.25

        )


        # ====================================================
        # UI PANEL
        # ====================================================

        cv2.rectangle(

            frame,

            (20, 20),

            (470, 265),

            (0, 0, 0),

            -1
        )


        cv2.putText(

            frame,

            "MOVECARE AI - SQUAT",

            (35, 55),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (255, 255, 255),

            2
        )


        cv2.putText(

            frame,

            f"REPS: {reps}",

            (35, 95),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (255, 255, 255),

            2
        )


        cv2.putText(

            frame,

            f"KNEE: {current_knee_angle:.0f} deg",

            (35, 130),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.6,

            (255, 255, 255),

            2
        )


        cv2.putText(

            frame,

            f"DEPTH: {depth_score:.0f}%",

            (35, 165),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.6,

            (255, 255, 255),

            2
        )


        cv2.putText(

            frame,

            f"KNEES: {knee_score:.0f}%",

            (35, 200),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.6,

            (255, 255, 255),

            2
        )


        cv2.putText(

            frame,

            f"TORSO: {torso_score:.0f}%",

            (35, 235),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.6,

            (255, 255, 255),

            2
        )


        # ====================================================
        # RIGHT SIDE
        # ====================================================

        cv2.putText(

            frame,

            f"FORM: {overall_score:.0f}%",

            (950, 55),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (255, 255, 255),

            2
        )


        cv2.putText(

            frame,

            f"STAGE: {stage}",

            (950, 90),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.6,

            (255, 255, 255),

            2
        )


        # ====================================================
        # FEEDBACK
        # ====================================================

        cv2.putText(

            frame,

            feedback,

            (800, 650),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (255, 255, 255),

            2
        )


    # ========================================================
    # NO PERSON
    # ========================================================

    else:

        cv2.putText(

            frame,

            "NO PERSON DETECTED",

            (420, 350),

            cv2.FONT_HERSHEY_SIMPLEX,

            1,

            (255, 255, 255),

            3
        )


    # ========================================================
    # DISPLAY
    # ========================================================

    cv2.imshow(

        WINDOW,

        frame
    )


    # ========================================================
    # QUIT
    # ========================================================

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):

        break


# ============================================================
# CLEANUP
# ============================================================

session_duration = time.time() - session_start

cap.release()

cv2.destroyAllWindows()

detector.close()


# ============================================================
# FINAL SCORES
# ============================================================

if depth_good_frames + depth_bad_frames > 0:

    final_depth_score = (

        depth_good_frames /
        (
            depth_good_frames +
            depth_bad_frames
        )

    ) * 100

else:

    final_depth_score = 100


if knee_good_frames + knee_bad_frames > 0:

    final_knee_score = (

        knee_good_frames /
        (
            knee_good_frames +
            knee_bad_frames
        )

    ) * 100

else:

    final_knee_score = 100


if torso_good_frames + torso_bad_frames > 0:

    final_torso_score = (

        torso_good_frames /
        (
            torso_good_frames +
            torso_bad_frames
        )

    ) * 100

else:

    final_torso_score = 100


final_overall_score = (

    final_depth_score * 0.40 +

    final_knee_score * 0.35 +

    final_torso_score * 0.25

)


# ============================================================
# RATING
# ============================================================

if final_overall_score >= 90:

    rating = "EXCELLENT"

elif final_overall_score >= 80:

    rating = "GOOD"

elif final_overall_score >= 70:

    rating = "FAIR"

elif final_overall_score >= 60:

    rating = "NEEDS IMPROVEMENT"

else:

    rating = "POOR"


# ============================================================
# ISSUES
# ============================================================

issues = []

recommendations = []


if shallow_squat_frames > 20:

    issues.append(
        "Squat depth was inconsistent."
    )

    recommendations.append(
        "Try to reach a deeper squat position."
    )


if knee_alignment_frames > 20:

    issues.append(
        "Knee alignment was inconsistent."
    )

    recommendations.append(
        "Keep both knees tracking consistently."
    )


if torso_lean_frames > 20:

    issues.append(
        "Excessive forward torso lean detected."
    )

    recommendations.append(
        "Keep your chest more upright during the squat."
    )


if not issues:

    issues.append(
        "No major form issues detected."
    )


if not recommendations:

    recommendations.append(
        "Continue maintaining your current squat technique."
    )


# ============================================================
# STRUCTURED RESULT
# ============================================================

exercise_result = {

    "exercise": "squat",

    "repetitions": reps,

    "duration_seconds": round(
        session_duration,
        2
    ),

    "scores": {

        "depth": round(
            final_depth_score,
            1
        ),

        "knee_alignment": round(
            final_knee_score,
            1
        ),

        "torso": round(
            final_torso_score,
            1
        ),

        "overall": round(
            final_overall_score,
            1
        )
    },

    "metrics": {

        "deepest_knee_angle": round(
            lowest_knee_angle,
            1
        )
    },

    "issues": issues,

    "recommendations": recommendations,

    "rating": rating
}


# ============================================================
# FINAL REPORT
# ============================================================

print("")
print("")
print("==========================================")
print("        MOVECARE AI - SQUAT REPORT")
print("==========================================")
print("")

print(
    f"Repetitions:          {reps}"
)

print(
    f"Duration:             {session_duration:.1f}s"
)

print("------------------------------------------")

print(
    f"Depth Score:          {final_depth_score:.0f}%"
)

print(
    f"Knee Alignment:       {final_knee_score:.0f}%"
)

print(
    f"Torso Score:          {final_torso_score:.0f}%"
)

print("------------------------------------------")

print(
    f"OVERALL FORM SCORE:   {final_overall_score:.0f}%"
)

print(
    f"RATING:               {rating}"
)

print("------------------------------------------")

print("")
print("ISSUES:")

for issue in issues:

    print(
        f"- {issue}"
    )


print("")
print("RECOMMENDATIONS:")

for recommendation in recommendations:

    print(
        f"- {recommendation}"
    )


print("")
print("==========================================")
print("           TEST COMPLETE")
print("==========================================")
print("")


# ============================================================
# DATA FOR AI REPORT / HISTORY
# ============================================================

print("")
print("EXERCISE RESULT:")
print(exercise_result)