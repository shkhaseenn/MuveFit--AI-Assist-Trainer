Yep — for the \*\*requirements file\*\*, use this for your MuveFit project.



I recommend:



```text

C:\\MoveCare\\Requirements.md

```



or, since you've been organizing docs, you can also keep it as:



```text

C:\\MoveCare\\docs\\REQUIREMENTS.md

```



For GitHub, I’d use `docs/REQUIREMENTS.md`.



Open it:



```powershell

notepad "C:\\MoveCare\\docs\\REQUIREMENTS.md"

```



Then paste \*\*everything below\*\*:



````md

\# MuveFit — Technical Requirements



\## 1. Project Requirements



MuveFit is a camera-based movement analysis platform that combines:



\- Camera/webcam input

\- Pose landmark detection

\- Exercise analysis

\- Form evaluation

\- Repetition and duration tracking

\- Movement feedback

\- Workout history

\- User profiles

\- AI safety awareness



The system must be modular so the frontend, backend, and exercise-analysis layers can be developed independently.



\---



\# 2. Frontend Requirements



\## Framework



The frontend shall use:



\- React

\- Vite

\- JavaScript

\- CSS



\## Frontend Structure



The frontend should contain:



```text

frontend/

└── src/

&#x20;   ├── App.jsx

&#x20;   ├── App.css

&#x20;   ├── components/

&#x20;   ├── pages/

&#x20;   ├── services/

&#x20;   └── hooks/

````



\## Required Screens



The frontend must support:



1\. Camera introduction

2\. Landing page

3\. Login

4\. Signup

5\. Dashboard

6\. Workout selection

7\. Live workout

8\. Workout result

9\. History

10\. Profile

11\. AI safety



\---



\# 3. Camera Requirements



The system must:



\* Request camera permission before using the camera.

\* Display the camera feed during workouts.

\* Detect whether a person is visible.

\* Provide feedback when the user is outside the expected frame.

\* Stop camera access when the workout ends.

\* Avoid permanent raw-video storage by default.



The camera experience should work with common laptop and desktop webcams.



Future mobile versions should support smartphone cameras.



\---



\# 4. Pose Detection Requirements



The movement-analysis layer must support pose landmark detection.



The initial implementation uses:



\* Python

\* MediaPipe

\* OpenCV

\* Pose landmark models



Relevant squat landmarks include:



```text

Shoulders

Hips

Knees

Ankles

```



The system should be able to obtain landmark coordinates and use them for movement calculations.



\---



\# 5. Exercise Requirements



Initial exercises:



```text

Squat

Plank

Burpee

Squat Hold

Glute Bridge

```



Each exercise should have:



\* Exercise identifier

\* Display name

\* Required landmarks

\* Movement rules

\* Metrics

\* State detection

\* Scoring

\* Feedback



New exercises should be addable without rewriting the whole application.



\---



\# 6. Squat Requirements



Squat is the initial AI proof-of-concept.



The system must calculate:



\* Left knee angle

\* Right knee angle

\* Average knee angle

\* Squat depth

\* Knee alignment

\* Torso angle

\* Repetitions

\* Form score



\---



\# 7. Squat Rep Detection



The intended repetition cycle is:



```text

UP

&#x20;↓

Knee angle <= 100°

&#x20;↓

DOWN

&#x20;↓

Knee angle >= 165°

&#x20;↓

REP + 1

&#x20;↓

UP

```



The system should use frame stability to reduce false state changes.



A repetition cooldown should help prevent duplicate counting.



\---



\# 8. Squat Depth Requirements



The current prototype uses:



```text

<= 100°

Deep enough



101°–120°

Needs more depth



121°–145°

Squat lower



146°–159°

Bend your knees



>= 160°

Standing / transition

```



These values are configurable and may be adjusted after testing.



\---



\# 9. Knee Alignment Requirements



The system should compare the left and right knee measurements.



Prototype interpretation:



```text

Difference <= 10°

Good alignment



Difference <= 20°

Needs attention



Difference > 20°

Alignment issue

```



The implementation should be configurable.



\---



\# 10. Torso Requirements



During a squat, the system should evaluate torso position using:



```text

Shoulder

&#x20;↓

Hip

&#x20;↓

Knee

```



Possible feedback:



```text

GOOD FORM

KEEP CHEST UP

REDUCE FORWARD LEAN

```



\---



\# 11. Form Scoring Requirements



The initial squat score should use:



```text

Depth              40%

Knee Alignment     35%

Torso               25%

```



Formula:



```text

Overall Score =

(depth × 0.40)

\+

(knee alignment × 0.35)

\+

(torso × 0.25)

```



Scores should be represented as percentages from 0–100.



\---



\# 12. Live Feedback Requirements



The system should provide short feedback while exercising.



Examples:



```text

GOOD FORM

GO DEEPER

SQUAT LOWER

BEND YOUR KNEES

CHECK KNEE ALIGNMENT

KNEES NOT ALIGNED

KEEP CHEST UP

REDUCE FORWARD LEAN

```



Feedback should not overwhelm the user with large amounts of text.



\---



\# 13. Workout Requirements



A workout session should contain:



\* User

\* Exercise

\* Start time

\* End time

\* Duration

\* Repetitions or hold duration

\* Live movement metrics

\* Final scores

\* Rating

\* Issues

\* Recommendations



Workout states:



```text

CREATED

STARTED

ANALYSING

COMPLETED

```



Possible alternate states:



```text

FAILED

CANCELLED

```



\---



\# 14. Workout Result Requirements



The exercise-analysis layer should return structured data.



Example:



```json

{

&#x20; "exercise": "squat",

&#x20; "repetitions": 12,

&#x20; "duration\_seconds": 48,

&#x20; "scores": {

&#x20;   "depth": 92,

&#x20;   "knee\_alignment": 89,

&#x20;   "torso": 93,

&#x20;   "overall": 91

&#x20; },

&#x20; "metrics": {

&#x20;   "deepest\_knee\_angle": 96

&#x20; },

&#x20; "issues": \[],

&#x20; "recommendations": \[

&#x20;   "Continue maintaining your current squat technique."

&#x20; ],

&#x20; "rating": "EXCELLENT"

}

```



\---



\# 15. Dashboard Requirements



The dashboard must contain:



\* Navbar

\* Sidebar

\* Welcome section

\* Movement scorecard

\* Motivation slider

\* Movement/skeleton preview

\* Quick workout actions



\---



\# 16. Dashboard Metrics



The scorecard should support:



```text

Form Score

Accuracy

Workouts

Streak

```



The prototype may use static values.



The production implementation must retrieve user-specific values from the backend.



\---



\# 17. Motivation Requirements



The dashboard must provide motivational content.



The prototype may use predefined messages.



Example:



```text

Consistency beats intensity.



Your movement is improving.



Focus on the next rep.



Move with intention.

```



Future versions may personalize these messages using workout history.



\---



\# 18. Movement Preview Requirements



The prototype may use a CSS-based movement visualization.



The production system should support:



```text

Camera

&#x20;↓

Pose Landmarks

&#x20;↓

Skeleton Renderer

&#x20;↓

Live Movement Visualization

```



The visualization should communicate movement sensing rather than medical anatomy.



\---



\# 19. History Requirements



The history system must support:



\* Previous workouts

\* Exercise name

\* Date

\* Repetitions/duration

\* Overall score

\* Rating



Future requirements may include:



\* Filters

\* Trends

\* Personal bests

\* Weekly statistics

\* Exercise comparisons



\---



\# 20. Profile Requirements



The profile system should support:



\* Name

\* Email

\* Workout count

\* Best form score

\* Streak

\* Camera preferences

\* History preferences

\* Privacy settings



\---



\# 21. Safety Requirements



The application must include a separate safety-awareness interface.



Users should be able to describe:



\* Pain

\* Discomfort

\* Fatigue

\* Movement difficulty

\* Recovery concerns



The system must clearly communicate:



> MuveFit is not a medical diagnosis system.



Urgent or serious symptoms should be directed toward qualified professional care.



\---



\# 22. Authentication Requirements



The backend authentication system should eventually support:



```text

POST /api/auth/register

POST /api/auth/login

POST /api/auth/logout

GET  /api/auth/me

```



The frontend should not permanently store sensitive credentials.



\---



\# 23. Backend Requirements



The backend must provide an API layer between the frontend and analysis services.



Responsibilities:



\* Authentication

\* User management

\* Workout sessions

\* History

\* Profiles

\* Safety

\* AI-service communication

\* Persistence

\* Authorization



\---



\# 24. API Requirements



Initial endpoints:



```text

Authentication



POST /api/auth/register

POST /api/auth/login

POST /api/auth/logout

GET  /api/auth/me





Exercises



GET /api/exercises





Workouts



POST /api/workouts/start

POST /api/workouts/{id}/finish

GET  /api/workouts

GET  /api/workouts/{id}





Analysis



POST /api/analysis/frame

POST /api/analysis/session





History



GET /api/history

GET /api/history/{id}





Profile



GET   /api/profile

PATCH /api/profile





Safety



POST /api/safety/check

```



Detailed endpoint definitions are documented in:



```text

docs/API.md

```



\---



\# 25. AI Service Requirements



The AI/exercise-analysis layer must:



\* Receive appropriate movement input.

\* Process pose landmarks.

\* Calculate exercise metrics.

\* Detect movement state.

\* Calculate scores.

\* Produce feedback.

\* Return structured JSON.



The AI layer should remain independent from the frontend.



\---



\# 26. Real-Time Requirements



During a live workout, the system should process movement continuously.



Conceptually:



```text

Camera Frame

&#x20;↓

Pose Detection

&#x20;↓

Movement Metrics

&#x20;↓

Exercise Logic

&#x20;↓

Feedback

&#x20;↓

Frontend

&#x20;↓

Next Frame

```



The system should prioritize low-latency feedback.



\---



\# 27. Privacy Requirements



MuveFit should follow a privacy-first approach.



The preferred data flow is:



```text

Camera Input

&#x20;↓

Movement Analysis

&#x20;↓

Structured Metrics

&#x20;↓

Optional History

```



Raw workout footage should not be stored permanently by default.



The system should clearly communicate camera usage to users.



\---



\# 28. Security Requirements



Production implementation should include:



\* Secure authentication

\* Password hashing

\* Authorization

\* Protected API endpoints

\* Input validation

\* Secure session/token management

\* Rate limiting where appropriate

\* Protection of user information



Secrets must not be committed to Git.



\---



\# 29. Error Handling Requirements



The application must gracefully handle:



\* Camera unavailable

\* Camera permission denied

\* No person detected

\* User outside frame

\* Poor pose visibility

\* Low landmark confidence

\* Backend unavailable

\* AI service unavailable

\* Network failure

\* Interrupted workout



The user should receive clear messages rather than technical stack traces.



\---



\# 30. Performance Requirements



The application should prioritize:



\* Responsive camera display

\* Low analysis latency

\* Efficient pose processing

\* Smooth frontend rendering

\* Reliable API communication



Performance should be evaluated particularly during live workout sessions.



\---



\# 31. Accessibility Requirements



The interface should provide:



\* Strong text contrast

\* Clear labels

\* Readable typography

\* Large interaction targets

\* Keyboard navigation where appropriate

\* Responsive layouts



Live workout information should remain readable while users are moving.



\---



\# 32. Responsive Requirements



\## Desktop



Support:



\* Large camera workspace

\* Sidebar

\* Detailed metrics

\* Dashboard panels



\## Tablet



Support:



\* Condensed navigation

\* Responsive content

\* Flexible camera area



\## Mobile



Support:



\* Mobile navigation

\* Full-screen camera workout

\* Large touch targets

\* Stacked metrics



\---



\# 33. Configuration Requirements



Configuration should eventually support:



```text

API\_URL

DATABASE\_URL

MODEL\_PATH

AUTH\_SETTINGS

CAMERA\_SETTINGS

```



Developer-specific paths should not be hardcoded into production code.



\---



\# 34. Testing Requirements



Testing should cover:



\## Frontend



\* Navigation

\* Authentication forms

\* Workout selection

\* Dashboard rendering

\* Responsive behavior



\## Backend



\* Authentication

\* API validation

\* Authorization

\* Workout lifecycle

\* History



\## Exercise / AI



\* Angle calculations

\* Rep detection

\* State transitions

\* Form scoring

\* Edge cases



\---



\# 35. Squat Test Cases



\### Test 1 — Standing



Expected:



```text

Stage = UP

```



\### Test 2 — Deep Squat



Expected:



```text

Stage = DOWN

```



\### Test 3 — Return to Standing



Expected:



```text

Rep + 1

```



\### Test 4 — Partial Squat



Expected:



```text

No completed repetition

```



\### Test 5 — No Person



Expected:



```text

NO PERSON DETECTED

```



\### Test 6 — Person Outside Frame



Expected:



```text

PLEASE MOVE INTO FRAME

```



\---



\# 36. Architecture Requirements



The system should maintain separation between:



```text

Frontend

↓

API

↓

Backend

↓

AI / Exercise Service

↓

Pose Model

```



Each layer should communicate through defined interfaces.



\---



\# 37. Maintainability Requirements



The system should:



\* Keep exercise logic modular.

\* Keep API contracts documented.

\* Avoid duplicated business logic.

\* Avoid hardcoded user data in production.

\* Keep configuration separate from implementation.

\* Maintain clear repository organization.



\---



\# 38. Scalability Requirements



The architecture should support:



\* Additional exercises

\* Additional movement metrics

\* More users

\* Additional AI models

\* Mobile clients

\* Personalized coaching

\* Expanded workout history



Adding a new exercise should not require rewriting the complete application.



\---



\# 39. Current Prototype Requirements



The current prototype should demonstrate:



```text

Camera Introduction

↓

Landing

↓

Login / Signup

↓

Dashboard

↓

Workout Selection

↓

Workout Screen

↓

History

↓

Profile

↓

Safety

```



The prototype may use:



\* Demo values

\* Static history

\* Frontend state

\* Placeholder movement visualization



\---



\# 40. Production Requirements



The production implementation should replace prototype placeholders with:



\* Real authentication

\* Persistent user accounts

\* Real camera processing

\* Real-time pose landmarks

\* Backend APIs

\* Persistent workout history

\* Real user-specific metrics

\* AI/exercise service integration

\* Production security



\---



\# 41. Definition of Done



The MVP is considered complete when a user can:



1\. Open MuveFit.

2\. Experience the camera introduction.

3\. Create or access an account.

4\. Enter the dashboard.

5\. Select an exercise.

6\. Allow camera access.

7\. Position themselves in frame.

8\. Perform the exercise.

9\. Receive movement/form feedback.

10\. Complete the workout.

11\. View the workout result.

12\. View the session in history.



\---



\# 42. Requirements Principle



The core technical principle is:



```text

Camera

&#x20;↓

Movement

&#x20;↓

Pose

&#x20;↓

Analysis

&#x20;↓

Feedback

&#x20;↓

Progress

```



The system should remain modular, privacy-conscious, responsive, and scalable while preserving this core experience.



````



Save it with \*\*Ctrl + S\*\*.



Then check:



```powershell

Get-Item "C:\\MoveCare\\docs\\REQUIREMENTS.md" | Select-Object Name,Length

````



Then:



```powershell

git -C C:\\MoveCare add docs/REQUIREMENTS.md

git -C C:\\MoveCare status --short

```



Your `docs` folder will now be:



```text

docs/

├── PRD.md

├── DESIGN.md

├── API.md

├── README.md

├── REQUIREMENTS.md

└── architecture/

&#x20;   └── system-architecture.md

```



That is a clean structure for your Git repo.



