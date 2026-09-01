\# MuveFit — API Documentation



\## 1. Overview



The MuveFit API connects the React frontend with the backend, exercise-analysis services, and future persistent data storage.



The intended flow is:



```text

React Frontend

&#x20;     ↓

Backend API

&#x20;     ↓

Exercise / AI Service

&#x20;     ↓

Python + MediaPipe

&#x20;     ↓

Movement Analysis

&#x20;     ↓

Structured Result

&#x20;     ↓

Backend

&#x20;     ↓

React UI



Yes. Let's do \*\*only `API.md` first\*\*.



Open it with:



```powershell

notepad "C:\\MoveCare\\docs\\API.md"

```



Delete anything currently inside it, then paste this:



````md

\# MuveFit — API Documentation



\## 1. Overview



The MuveFit API connects the React frontend with the backend, exercise-analysis services, and future persistent data storage.



The intended flow is:



```text

React Frontend

&#x20;     ↓

Backend API

&#x20;     ↓

Exercise / AI Service

&#x20;     ↓

Python + MediaPipe

&#x20;     ↓

Movement Analysis

&#x20;     ↓

Structured Result

&#x20;     ↓

Backend

&#x20;     ↓

React UI

````



The API is designed to keep the frontend independent from the internal implementation of the exercise-analysis engine.



\---



\# 2. API Base URL



Development:



```text

http://localhost:8000

```



Production:



```text

TBD

```



The production API URL will be defined when backend deployment is configured.



\---



\# 3. Authentication



Authentication will be handled by the backend.



\## Register



```http

POST /api/auth/register

```



\### Request



```json

{

&#x20; "name": "User Name",

&#x20; "email": "user@example.com",

&#x20; "password": "password"

}

```



\### Response



```json

{

&#x20; "message": "Account created",

&#x20; "user": {

&#x20;   "id": "user-id",

&#x20;   "name": "User Name",

&#x20;   "email": "user@example.com"

&#x20; }

}

```



\---



\## Login



```http

POST /api/auth/login

```



\### Request



```json

{

&#x20; "email": "user@example.com",

&#x20; "password": "password"

}

```



\### Response



```json

{

&#x20; "message": "Login successful",

&#x20; "user": {

&#x20;   "id": "user-id",

&#x20;   "name": "User Name",

&#x20;   "email": "user@example.com"

&#x20; }

}

```



\---



\## Current User



```http

GET /api/auth/me

```



Returns the currently authenticated user.



Example:



```json

{

&#x20; "id": "user-id",

&#x20; "name": "User Name",

&#x20; "email": "user@example.com"

}

```



\---



\## Logout



```http

POST /api/auth/logout

```



Example response:



```json

{

&#x20; "message": "Logged out successfully"

}

```



\---



\# 4. Exercises



\## Get Available Exercises



```http

GET /api/exercises

```



\### Response



```json

{

&#x20; "exercises": \[

&#x20;   {

&#x20;     "id": "squat",

&#x20;     "name": "Squat",

&#x20;     "metric": "REPS",

&#x20;     "focus": \[

&#x20;       "depth",

&#x20;       "knee alignment",

&#x20;       "torso"

&#x20;     ]

&#x20;   },

&#x20;   {

&#x20;     "id": "plank",

&#x20;     "name": "Plank",

&#x20;     "metric": "TIME",

&#x20;     "focus": \[

&#x20;       "alignment",

&#x20;       "stability"

&#x20;     ]

&#x20;   },

&#x20;   {

&#x20;     "id": "burpee",

&#x20;     "name": "Burpee",

&#x20;     "metric": "REPS",

&#x20;     "focus": \[

&#x20;       "jump",

&#x20;       "landing",

&#x20;       "rhythm"

&#x20;     ]

&#x20;   },

&#x20;   {

&#x20;     "id": "squat-hold",

&#x20;     "name": "Squat Hold",

&#x20;     "metric": "TIME",

&#x20;     "focus": \[

&#x20;       "depth",

&#x20;       "stability",

&#x20;       "duration"

&#x20;     ]

&#x20;   },

&#x20;   {

&#x20;     "id": "glute-bridge",

&#x20;     "name": "Glute Bridge",

&#x20;     "metric": "REPS",

&#x20;     "focus": \[

&#x20;       "hip alignment",

&#x20;       "control"

&#x20;     ]

&#x20;   }

&#x20; ]

}

```



\---



\# 5. Workout Sessions



\## Start Workout



```http

POST /api/workouts/start

```



\### Request



```json

{

&#x20; "exercise": "squat"

}

```



\### Response



```json

{

&#x20; "workout\_id": "workout-id",

&#x20; "exercise": "squat",

&#x20; "status": "started",

&#x20; "started\_at": "2026-09-02T12:00:00Z"

}

```



\---



\## Finish Workout



```http

POST /api/workouts/{workout\_id}/finish

```



\### Request



```json

{

&#x20; "duration\_seconds": 48

}

```



\### Response



```json

{

&#x20; "workout\_id": "workout-id",

&#x20; "status": "completed"

}

```



\---



\## Get Workout Sessions



```http

GET /api/workouts

```



Returns the user's previous workout sessions.



\---



\## Get Specific Workout



```http

GET /api/workouts/{workout\_id}

```



Returns one completed workout and its analysis result.



\---



\# 6. Movement Analysis



The movement-analysis API connects the backend to the exercise-analysis service.



\## Analyze Frame



```http

POST /api/analysis/frame

```



The exact frame transport format will be finalized during camera/backend integration.



The service may receive:



\* Camera frame

\* Exercise identifier

\* Session identifier

\* Timestamp



Example conceptual request:



```json

{

&#x20; "workout\_id": "workout-id",

&#x20; "exercise": "squat",

&#x20; "timestamp\_ms": 123456

}

```



\---



\## Analyze Session



```http

POST /api/analysis/session

```



This endpoint can be used to process or finalize a complete exercise session.



Example request:



```json

{

&#x20; "workout\_id": "workout-id",

&#x20; "exercise": "squat"

}

```



\---



\# 7. Exercise Analysis Result



The exercise-analysis service returns structured movement information.



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



\# 8. Squat Analysis



The initial AI implementation focuses on squat analysis.



The current squat engine evaluates:



\* Knee angle

\* Squat depth

\* Knee alignment

\* Torso position

\* Repetitions

\* Form score



\## Squat Rep Logic



Conceptually:



```text

Standing

&#x20;  ↓

Knee angle <= 100°

&#x20;  ↓

DOWN

&#x20;  ↓

Knee angle >= 165°

&#x20;  ↓

REP + 1

```



The exercise-analysis service is responsible for the movement logic.



The frontend should only consume the resulting structured data.



\---



\# 9. Live Feedback



The backend/analysis service may return short feedback messages.



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



These messages are intended for live workout display.



\---



\# 10. History



\## Get History



```http

GET /api/history

```



Example response:



```json

{

&#x20; "sessions": \[

&#x20;   {

&#x20;     "id": "workout-1",

&#x20;     "date": "2026-09-02",

&#x20;     "exercise": "squat",

&#x20;     "repetitions": 12,

&#x20;     "score": 91,

&#x20;     "rating": "EXCELLENT"

&#x20;   },

&#x20;   {

&#x20;     "id": "workout-2",

&#x20;     "date": "2026-09-01",

&#x20;     "exercise": "plank",

&#x20;     "duration\_seconds": 42,

&#x20;     "score": 88,

&#x20;     "rating": "GOOD"

&#x20;   }

&#x20; ]

}

```



\---



\## Get History Item



```http

GET /api/history/{workout\_id}

```



Returns the detailed workout result.



\---



\# 11. Profile



\## Get Profile



```http

GET /api/profile

```



Example response:



```json

{

&#x20; "name": "User Name",

&#x20; "email": "user@example.com",

&#x20; "statistics": {

&#x20;   "workouts": 24,

&#x20;   "best\_form": 96,

&#x20;   "streak": 6

&#x20; }

}

```



\---



\## Update Profile



```http

PATCH /api/profile

```



Example request:



```json

{

&#x20; "name": "Updated Name",

&#x20; "email": "updated@example.com"

}

```



\---



\# 12. Safety



\## Submit Safety Check



```http

POST /api/safety/check

```



Example request:



```json

{

&#x20; "message": "My knee feels uncomfortable during squats."

}

```



Example response structure:



```json

{

&#x20; "status": "received",

&#x20; "message": "Your concern has been received for review."

}

```



The final safety-response system will be defined during AI/backend implementation.



MuveFit must clearly communicate that it is not a medical diagnosis system.



\---



\# 13. Error Format



The API should use a consistent error structure.



Example:



```json

{

&#x20; "error": {

&#x20;   "code": "INVALID\_REQUEST",

&#x20;   "message": "The provided request is invalid."

&#x20; }

}

```



\---



\# 14. HTTP Status Codes



Expected status codes:



```text

200 OK

201 Created

400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

422 Validation Error

500 Internal Server Error

```



\---



\# 15. Privacy



The API should follow the product's privacy-first architecture.



Preferred flow:



```text

Camera

&#x20;  ↓

Movement Analysis

&#x20;  ↓

Structured Metrics

&#x20;  ↓

Optional History Storage

```



Raw workout footage should not be permanently stored by default.



The backend should only retain data required for product functionality and user history.



\---



\# 16. Authentication and Protected Routes



Protected endpoints should require an authenticated user.



Protected areas include:



```text

/api/workouts

/api/history

/api/profile

/api/analysis

```



Public endpoints may include:



```text

/api/auth/register

/api/auth/login

/api/exercises

```



The final authentication mechanism will be selected during backend implementation.



\---



\# 17. Frontend Integration



The React frontend should communicate with the backend through a dedicated service layer.



Suggested frontend structure:



```text

src/

├── services/

│   ├── api.js

│   ├── auth.js

│   └── workouts.js

```



The UI should not contain hardcoded backend implementation logic.



\---



\# 18. Backend Integration Flow



The intended workout flow is:



```text

User

&#x20;↓

React Camera

&#x20;↓

Workout Session

&#x20;↓

Backend API

&#x20;↓

Exercise Analysis

&#x20;↓

Pose / Movement Model

&#x20;↓

Analysis Result

&#x20;↓

Backend

&#x20;↓

React Live UI

&#x20;↓

Workout Report

&#x20;↓

History

```



\---



\# 19. Current Development Status



\## Implemented / Prototype



\* Frontend navigation

\* Landing page

\* Authentication UI

\* Dashboard UI

\* Workout selection

\* History UI

\* Profile UI

\* Safety UI

\* Python squat-analysis prototype



\## In Progress



\* Backend API implementation

\* Real camera integration

\* Frontend/backend communication

\* Live pose data

\* Persistent workout history

\* Authentication persistence



\## Future



\* Additional exercise-analysis services

\* Personalized coaching

\* Advanced movement metrics

\* Recovery insights

\* Mobile application integration



\---



\# 20. API Design Principles



The MuveFit API should:



1\. Keep the frontend independent from AI implementation details.

2\. Return predictable JSON structures.

3\. Validate all incoming data.

4\. Protect user-specific resources.

5\. Minimize unnecessary storage of camera data.

6\. Keep exercise analysis modular.

7\. Allow new exercises to be added without redesigning the entire API.



````



Then save with:



```text

Ctrl + S

````



After saving, \*\*don't add anything else yet\*\*.



Check that it worked:



```powershell

Get-Item "C:\\MoveCare\\docs\\API.md" | Select-Object Name,Length

```



Then:



```powershell

git -C C:\\MoveCare status --short

```



You should see `docs/API.md` as changed/new.



