Yes. Since you moved architecture under `docs`, make it:

```text
C:\MoveCare\docs\
├── PRD.md
├── DESIGN.md
├── API.md
├── README.md
└── architecture\
    └── system-architecture.md
```

Open the architecture file:

```powershell
notepad "C:\MoveCare\docs\architecture\system-architecture.md"
```

Delete what is there and paste this **entire architecture document**:

````md
# MuveFit — System Architecture

## 1. Purpose

This document defines the technical architecture of MuveFit and explains how the frontend, backend, exercise-analysis services, AI/pose models, camera input, and stored workout data are intended to work together.

The architecture is designed to keep the user interface, backend services, and movement-analysis logic separate so each layer can evolve independently.

---

# 2. System Overview

MuveFit is a camera-based movement analysis platform.

The high-level system flow is:

```text
USER
  ↓
CAMERA / WEBCAM
  ↓
REACT FRONTEND
  ↓
BACKEND API
  ↓
EXERCISE / AI SERVICE
  ↓
POSE DETECTION
  ↓
MOVEMENT ANALYSIS
  ↓
STRUCTURED EXERCISE RESULT
  ↓
BACKEND
  ↓
DATABASE / HISTORY
  ↓
REACT DASHBOARD / REPORT
````

---

# 3. Repository Structure

The repository is organized into separate technical responsibilities.

```text
MoveCare/
│
├── ai-engine/
├── backend/
├── docs/
│   ├── PRD.md
│   ├── DESIGN.md
│   ├── API.md
│   ├── README.md
│   └── architecture/
│       └── system-architecture.md
│
├── exercises/
├── frontend/
├── models/
└── .gitignore
```

---

# 4. Directory Responsibilities

## ai-engine/

Contains AI and movement-intelligence services.

Potential responsibilities:

* Movement inference
* Exercise intelligence
* Form analysis
* Recommendation logic
* Future AI coaching

---

## backend/

Contains server-side application logic and API endpoints.

Responsibilities:

* Authentication
* User management
* Workout sessions
* API routing
* History
* Profile data
* Database access
* AI-service communication
* Security

---

## docs/

Contains project documentation.

```text
docs/
├── PRD.md
├── DESIGN.md
├── API.md
├── README.md
└── architecture/
    └── system-architecture.md
```

### PRD.md

Defines product requirements, goals, users, workflows, MVP, and future features.

### DESIGN.md

Defines the visual system and user-interface design.

### API.md

Defines backend endpoints and data contracts.

### README.md

Provides a project-level overview.

### architecture/

Contains technical architecture documentation.

---

## exercises/

Contains exercise-specific Python movement-analysis scripts.

Initial exercises include:

```text
Squat
Plank
Burpee
Squat Hold
Glute Bridge
```

The exercise layer contains logic specific to individual movements.

---

## frontend/

Contains the React/Vite application.

Responsibilities:

* Landing page
* Camera introduction
* Authentication UI
* Dashboard
* Workout selection
* Workout camera interface
* Live feedback
* History
* Profile
* Safety interface

---

## models/

Contains pose-analysis model assets.

Model files are kept separate from application source code.

---

# 5. Frontend Architecture

The frontend is responsible for the user experience.

Conceptually:

```text
React Application
│
├── Landing
├── Authentication
├── Dashboard
├── Workout Selection
├── Workout Camera
├── Results
├── History
├── Profile
└── Safety
```

The frontend handles:

* User interaction
* Navigation
* Visualisation
* Camera presentation
* Movement feedback
* Reports

The frontend should not directly depend on internal Python implementation details.

---

# 6. Frontend Navigation

The current product flow is:

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
Workout Camera
        ↓
Workout Result
        ↓
History
```

Dashboard destinations include:

```text
Dashboard
├── Workout
├── History
├── Safety
└── Profile
```

---

# 7. Camera Introduction Architecture

The opening sequence is a product-branding experience rather than an analysis process.

```text
Dark Screen
     ↓
Camera Appears
     ↓
Lens Zoom
     ↓
Shutter
     ↓
Flash
     ↓
MuveFit Logo
     ↓
Landing Page
```

The camera introduction may contain:

* Camera body
* Lens rings
* Aperture
* Glass reflections
* Vignette
* Lens zoom
* Shutter sound

---

# 8. Authentication Architecture

Authentication separates the public experience from the authenticated application.

Prototype:

```text
Login / Signup
      ↓
Frontend State
      ↓
Dashboard
```

Production:

```text
Login / Signup
      ↓
Backend API
      ↓
Authentication Service
      ↓
Authenticated Session
      ↓
Dashboard
```

The backend should be responsible for validating credentials and managing user sessions.

---

# 9. Dashboard Architecture

The dashboard is the main authenticated workspace.

```text
Dashboard
│
├── Navbar
├── Sidebar
│
└── Main
    ├── Welcome
    ├── Scorecard
    ├── Motivation Slider
    ├── Movement Preview
    └── Quick Actions
```

---

# 10. Dashboard Scorecard

The scorecard displays high-level movement information.

Main values:

```text
FORM SCORE
ACCURACY
WORKOUTS
STREAK
```

Prototype values may be static.

Production values should come from the backend.

Example:

```json
{
  "form_score": 91,
  "accuracy": 94,
  "workouts": 24,
  "streak": 6
}
```

---

# 11. Motivation Architecture

The motivation slider is initially frontend-driven.

Prototype:

```text
Static Messages
      ↓
React State
      ↓
Slider
```

Future:

```text
Workout History
      ↓
Progress Analysis
      ↓
Personalized Message
      ↓
Motivation UI
```

---

# 12. Movement Preview Architecture

The dashboard prototype includes a stylized movement/skeleton preview.

Prototype:

```text
CSS Movement Visualization
        ↓
Dashboard
```

Production:

```text
Camera
  ↓
Pose Detection
  ↓
Landmarks
  ↓
Movement Renderer
  ↓
Frontend
```

The production preview should visualize real body landmarks.

---

# 13. Workout Architecture

The workout system follows:

```text
Exercise Selection
        ↓
Workout Session
        ↓
Camera Permission
        ↓
Camera Feed
        ↓
Pose Detection
        ↓
Movement Analysis
        ↓
Live Feedback
        ↓
Workout Completion
        ↓
Workout Result
```

---

# 14. Exercise Architecture

Each exercise should have its own analysis logic.

Example:

```text
Squat
├── Landmark requirements
├── Joint angles
├── Depth
├── Alignment
├── Stability
├── State machine
├── Rep detection
├── Scoring
└── Feedback
```

The same general architecture can be applied to future exercises.

---

# 15. Pose Detection Architecture

The pose system converts image data into body landmarks.

```text
Camera Frame
      ↓
Image Processing
      ↓
Pose Model
      ↓
Body Landmarks
```

Relevant squat landmarks include:

```text
Shoulder
Hip
Knee
Ankle
```

These landmarks are used for movement calculations.

---

# 16. MediaPipe Architecture

The current movement-analysis implementation uses MediaPipe pose landmarks.

Conceptually:

```text
Python
  ↓
MediaPipe
  ↓
Pose Model
  ↓
Body Landmarks
```

The AI/exercise layer should hide the model implementation from the frontend.

---

# 17. Squat Analysis Pipeline

The initial AI focus is squat analysis.

The processing pipeline is:

```text
Camera Frame
      ↓
Pose Detection
      ↓
Landmark Extraction
      ↓
Hip / Knee / Ankle Points
      ↓
Knee Angle Calculation
      ↓
Depth Evaluation
      ↓
Knee Alignment
      ↓
Torso Evaluation
      ↓
Rep State Detection
      ↓
Form Scoring
      ↓
Feedback
      ↓
Structured Result
```

---

# 18. Knee Angle Calculation

The squat knee angle is calculated using:

```text
Hip
 ↓
Knee
 ↓
Ankle
```

Example:

```text
Left Knee  = 96°
Right Knee = 98°
Average    = 97°
```

The exact values come from the live pose landmarks.

---

# 19. Squat Rep State Machine

The intended squat repetition flow is:

```text
UP
 ↓
Knee angle <= 100°
 ↓
DOWN
 ↓
Knee angle >= 165°
 ↓
REP + 1
 ↓
UP
```

Multiple frames can be required before changing states in order to reduce noise.

A cooldown can reduce accidental duplicate repetitions.

---

# 20. Squat Depth

The current prototype uses:

```text
<= 100°
Deep enough

101°–120°
Needs more depth

121°–145°
Squat lower

146°–159°
Bend knees

>= 160°
Standing / transition
```

These values are prototype thresholds and can be refined during testing.

---

# 21. Knee Alignment

The prototype compares left and right knee measurements.

Conceptual scoring:

```text
Difference <= 10°
     ↓
Good

Difference <= 20°
     ↓
Moderate issue

Difference > 20°
     ↓
Alignment issue
```

The exact implementation remains inside the exercise-analysis service.

---

# 22. Torso Analysis

Torso analysis uses:

```text
Shoulder
 ↓
Hip
 ↓
Knee
```

Possible classifications:

```text
Good
Needs adjustment
Excessive forward lean
```

---

# 23. Form Scoring

The current squat prototype uses:

```text
Depth              40%
Knee Alignment     35%
Torso               25%
```

Overall score:

```text
Overall =
(depth × 0.40)
+
(knee alignment × 0.35)
+
(torso × 0.25)
```

---

# 24. Feedback Architecture

The analysis layer provides short feedback messages.

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

Live feedback should remain concise.

Detailed explanations belong in the workout report.

---

# 25. Exercise Result Contract

The exercise-analysis service returns structured information.

Example:

```json
{
  "exercise": "squat",
  "repetitions": 12,
  "duration_seconds": 48,
  "scores": {
    "depth": 92,
    "knee_alignment": 89,
    "torso": 93,
    "overall": 91
  },
  "metrics": {
    "deepest_knee_angle": 96
  },
  "issues": [],
  "recommendations": [
    "Continue maintaining your current squat technique."
  ],
  "rating": "EXCELLENT"
}
```

This data contract allows different frontend implementations to use the same analysis result.

---

# 26. Backend Architecture

The backend acts as the main service boundary.

```text
Frontend
   ↓
Backend API
   ↓
Business Logic
   ├── Authentication
   ├── Workouts
   ├── History
   ├── Profile
   └── Safety
```

The backend also communicates with the exercise/AI layer.

---

# 27. Backend + AI Architecture

Preferred architecture:

```text
React
  ↓
Backend API
  ↓
Exercise / AI Service
  ↓
Python
  ↓
MediaPipe
  ↓
Pose Analysis
  ↓
Structured Result
  ↓
Backend
  ↓
React
```

This keeps frontend code independent from the Python implementation.

---

# 28. API Boundary

The frontend and backend communicate through defined API endpoints.

Examples:

```text
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me

GET  /api/exercises

POST /api/workouts/start
POST /api/workouts/{id}/finish
GET  /api/workouts
GET  /api/workouts/{id}

POST /api/analysis/frame
POST /api/analysis/session

GET  /api/history
GET  /api/history/{id}

GET   /api/profile
PATCH /api/profile

POST /api/safety/check
```

Detailed API definitions are documented in:

```text
docs/API.md
```

---

# 29. Database Architecture

The production backend requires persistent storage.

Conceptually:

```text
Database
│
├── Users
├── Workouts
├── Exercise Results
├── History
└── User Preferences
```

A workout record may contain:

```text
Workout ID
User ID
Exercise
Date
Duration
Repetitions
Scores
Rating
Issues
Recommendations
```

The exact database technology can be selected during backend implementation.

---

# 30. User Data Flow

For an authenticated workout:

```text
User
 ↓
Authentication
 ↓
Workout Session
 ↓
Camera Analysis
 ↓
Result
 ↓
Backend
 ↓
Database
 ↓
History
```

---

# 31. Live Data vs Stored Data

## Live Data

Examples:

* Current pose
* Current knee angle
* Current stage
* Current feedback
* Current rep state

## Stored Data

Examples:

* Final repetition count
* Final score
* Duration
* Rating
* Issues
* Recommendations

This separation limits unnecessary storage.

---

# 32. Privacy Architecture

MuveFit follows a privacy-first model.

Preferred flow:

```text
Camera Input
     ↓
Movement Analysis
     ↓
Structured Metrics
     ↓
Optional History
```

Raw workout footage should not be permanently stored by default.

Structured workout results may be retained for:

* History
* Progress
* Reports
* Statistics

---

# 33. Camera Privacy

Camera access requires user permission.

The system should:

* Explain why camera access is needed.
* Request permission explicitly.
* Stop camera access after the workout.
* Avoid permanent raw-video storage by default.
* Minimize unnecessary camera data retention.

---

# 34. Safety Architecture

The safety feature is separate from exercise scoring.

Flow:

```text
User Concern
      ↓
Safety Interface
      ↓
Backend
      ↓
Safety Logic / Future AI
      ↓
Response
```

The application should clearly communicate:

> MuveFit is not a medical diagnosis system.

---

# 35. Security Architecture

The production system should include:

* Secure authentication
* Password protection
* Protected API endpoints
* Authorization checks
* Input validation
* Secure sessions/tokens
* Rate limiting where appropriate
* Protected service endpoints

Sensitive user information should not be unnecessarily exposed to the frontend.

---

# 36. Error Handling

Each layer should handle its own failures.

```text
Camera Error
     ↓
Frontend Camera Message

Pose Error
     ↓
Analysis Error Message

API Error
     ↓
Backend Response

Database Error
     ↓
Backend Error Handling
```

A failure in one component should not unnecessarily crash the entire application.

---

# 37. Real-Time Analysis

The workout interface requires responsive movement feedback.

Conceptually:

```text
Camera Frame
     ↓
Pose Detection
     ↓
Movement Metric
     ↓
Feedback
     ↓
UI
     ↓
Next Frame
```

This cycle continues during a live workout.

---

# 38. Workout Session Lifecycle

A workout can move through:

```text
CREATED
   ↓
STARTED
   ↓
ANALYSING
   ↓
COMPLETED
```

Possible alternate states:

```text
FAILED
CANCELLED
```

---

# 39. Frontend / Backend Separation

## Frontend

Responsible for:

```text
UI
Navigation
Interaction
Camera presentation
Visualization
Live feedback
```

## Backend

Responsible for:

```text
Authentication
Persistence
Business logic
API
User data
Workout records
```

## AI / Exercise Layer

Responsible for:

```text
Pose processing
Movement metrics
Exercise rules
Rep detection
Form scoring
Feedback
```

---

# 40. Service Boundaries

Long-term architecture:

```text
Frontend
    │
    ▼
Backend / API
    │
    ├─────────────→ Authentication
    │
    ├─────────────→ Workout Service
    │
    ├─────────────→ History Service
    │
    ├─────────────→ Profile Service
    │
    ├─────────────→ Safety Service
    │
    └─────────────→ Exercise / AI Service
                              │
                              ▼
                       Pose / MediaPipe
```

During the prototype phase, some services may remain inside the same backend application.

---

# 41. Exercise Extensibility

The system should allow new exercise models to be added without rewriting the whole platform.

Conceptually:

```text
Exercise Registry
│
├── Squat
├── Plank
├── Burpee
├── Squat Hold
└── Glute Bridge
```

Each exercise follows:

```text
Input
 ↓
Analysis
 ↓
Metrics
 ↓
Feedback
 ↓
Result
```

---

# 42. Exercise Module Structure

A future exercise module can contain:

```text
Exercise
├── Metadata
├── Required Landmarks
├── Movement Rules
├── Metrics
├── State Machine
├── Scoring
└── Feedback
```

This provides a consistent interface for future exercises.

---

# 43. Model Management

Pose-analysis models are stored separately from application source code.

The application should reference model locations through configuration.

Model paths should not be tightly coupled to a developer's local machine.

---

# 44. Configuration

Production configuration may include:

```text
API_URL
DATABASE_URL
MODEL_PATH
AUTH_SETTINGS
CAMERA_SETTINGS
```

Secrets and credentials must not be committed to Git.

---

# 45. Development Environment

During development:

```text
Browser
   ↓
Vite Frontend
localhost:5173
   ↓
Backend
localhost:8000
   ↓
Exercise / AI Service
```

Exact ports may change depending on backend configuration.

---

# 46. Production Environment

Production architecture may look like:

```text
User
 ↓
HTTPS
 ↓
Frontend
 ↓
Backend API
 ↓
Authentication
 ↓
Database
 ↓
AI / Exercise Service
 ↓
Pose Models
```

---

# 47. Prototype Architecture

The current prototype simplifies some production infrastructure.

Frontend:

```text
React
 ↓
Frontend State
 ↓
Demo Data
```

Exercise analysis:

```text
Python
 ↓
MediaPipe
 ↓
Local Exercise Result
```

Production:

```text
React
 ↓
Backend API
 ↓
AI / Exercise Service
 ↓
Persistent Storage
```

---

# 48. Real Camera Integration

The intended production workout flow is:

```text
Browser Camera
      ↓
Camera Permission
      ↓
Live Video
      ↓
Pose Detection
      ↓
Landmarks
      ↓
Exercise Analysis
      ↓
Live Metrics
      ↓
Feedback
```

The exact transport mechanism between browser and backend/AI service will be finalized during implementation.

---

# 49. Testing Architecture

Testing should eventually cover all layers.

## Frontend

* Navigation
* Components
* Forms
* Camera states
* Responsive layouts

## Backend

* Authentication
* API validation
* Authorization
* Workout lifecycle
* History

## Exercise / AI

* Landmark calculations
* Joint angles
* Rep detection
* Scoring
* Edge cases

---

# 50. Squat Testing

Expected scenarios:

## Standing

```text
Stage = UP
```

## Deep Squat

```text
Stage = DOWN
```

## Return to Standing

```text
Rep + 1
```

## Partial Squat

```text
No completed rep
```

## No Person

```text
NO PERSON DETECTED
```

---

# 51. Failure Cases

The system should handle:

* Camera unavailable
* Camera permission denied
* No person detected
* Person partly outside frame
* Poor pose visibility
* Low landmark confidence
* Backend unavailable
* AI service unavailable
* Interrupted workout
* Network failure

User-facing messages should remain understandable.

---

# 52. Performance

Important performance factors include:

* Camera frame rate
* Pose inference time
* API latency
* Backend processing
* Frontend rendering
* Network conditions

The live workout experience should receive priority during optimization.

---

# 53. Accessibility

The application should support:

* Clear labels
* Readable text
* Strong contrast
* Large interaction targets
* Keyboard interaction where appropriate
* Responsive layouts

The live workout UI should remain readable while users are physically moving.

---

# 54. Desktop Architecture

The desktop experience is optimized for:

* Large camera workspace
* Sidebar navigation
* Detailed metrics
* Movement visualisation
* Dashboard panels

---

# 55. Mobile Architecture

The future mobile application can use the same conceptual system:

```text
Mobile Camera
      ↓
Mobile Frontend
      ↓
Backend API
      ↓
AI / Exercise Service
```

The interface can change for mobile without changing the overall data architecture.

---

# 56. Deployment Independence

Each major layer should be independently maintainable.

For example:

```text
React UI
```

can change without rewriting:

```text
Python Squat Analysis
```

as long as their data contract remains stable.

---

# 57. Data Contract Principle

Communication between services should rely on structured data.

Example:

```json
{
  "exercise": "squat",
  "repetitions": 12,
  "scores": {
    "overall": 91
  },
  "feedback": "GOOD FORM"
}
```

This makes the system easier to extend.

---

# 58. Scalability

The architecture should support:

* Additional exercises
* Additional pose models
* New feedback systems
* Personalized coaching
* Expanded history
* New client applications
* Mobile applications

The core API/data contract should remain stable wherever possible.

---

# 59. Technical Principles

## Separation of Concerns

Each layer should have a clear responsibility.

## Modularity

Exercise logic should be independently extendable.

## Data Contracts

Services should communicate through predictable structures.

## Privacy

Camera data should be minimized and raw footage should not be permanently stored by default.

## Maintainability

Frontend, backend, AI, and exercise logic should remain separated.

## Scalability

New exercises and services should be addable without rebuilding the entire platform.

---

# 60. Final System Diagram

```text
                              USER
                               │
                               ▼
                        CAMERA / WEBCAM
                               │
                               ▼
                    ┌────────────────────┐
                    │   REACT FRONTEND   │
                    │      + VITE        │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │     BACKEND API    │
                    └─────────┬──────────┘
                              │
              ┌───────────────┼────────────────┐
              │               │                │
              ▼               ▼                ▼
      ┌──────────────┐ ┌──────────────┐ ┌─────────────────┐
      │Authentication│ │   Database   │ │ Exercise / AI   │
      │   Service    │ │              │ │     Service     │
      └──────────────┘ └──────────────┘ └────────┬────────┘
                                                 │
                                                 ▼
                                        ┌─────────────────┐
                                        │ Python /         │
                                        │ MediaPipe       │
                                        └────────┬────────┘
                                                 │
                                                 ▼
                                        ┌─────────────────┐
                                        │ Pose Landmarks  │
                                        └────────┬────────┘
                                                 │
                                                 ▼
                                        ┌─────────────────┐
                                        │ Movement        │
                                        │ Analysis        │
                                        └────────┬────────┘
                                                 │
                                                 ▼
                                        ┌─────────────────┐
                                        │ Structured      │
                                        │ Result          │
                                        └────────┬────────┘
                                                 │
                                                 ▼
                                           BACKEND API
                                                 │
                                                 ▼
                                          REACT FRONTEND
                                                 │
                         ┌───────────────────────┼───────────────────────┐
                         │                       │                       │
                         ▼                       ▼                       ▼
                  Live Feedback             Report                  History
```

---

# 61. Current State

The current project contains:

* React/Vite frontend
* Camera introduction
* Landing page
* Authentication UI
* Dashboard
* Workout selection
* Workout interface
* History interface
* Profile interface
* Safety interface
* Constellation visuals
* Python exercise-analysis scripts
* Pose-model assets
* Product documentation

---

# 62. Current AI Focus

The first movement-analysis proof of concept is squat analysis.

Current focus:

```text
Pose Detection
↓
Knee Angle
↓
Depth
↓
Knee Alignment
↓
Torso
↓
Rep Detection
↓
Form Score
```

---

# 63. Future State

The intended future system includes:

* Production authentication
* Persistent user accounts
* Real webcam integration
* Real-time pose visualization
* Backend API integration
* AI service integration
* Persistent workout history
* Personalized insights
* Additional exercises
* Mobile application
* Production deployment

---

# 64. Final Architecture Principle

MuveFit maintains the following separation:

```text
USER EXPERIENCE
       ↓
FRONTEND
       ↓
API
       ↓
BACKEND
       ↓
AI / EXERCISE SERVICE
       ↓
POSE / MOVEMENT ANALYSIS
       ↓
STRUCTURED DATA
       ↓
HISTORY / INSIGHTS
```

The purpose of this architecture is to turn camera-observed movement into useful, understandable exercise insight while keeping the product modular, privacy-conscious, and extensible.

````

Then save with:

```text
Ctrl + S
````

Finally check the file exists:

```powershell
Get-Item "C:\MoveCare\docs\architecture\system-architecture.md" | Select-Object Name,Length
```

Then stage the move/update:

```powershell
git -C C:\MoveCare add -A
```

and check:

```powershell
git -C C:\MoveCare status --short
```

**Don't push yet.** The status output will tell us whether Git correctly sees the architecture inside `docs`.
