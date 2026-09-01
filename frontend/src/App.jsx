import { useEffect, useState } from "react";
import "./App.css";


/* ============================================================
   CAMERA SHUTTER SOUND
============================================================ */

function playShutterSound() {
  try {
    const sound = new Audio(
      "/sounds/camera-shutter.mp3"
    );

    sound.volume = 0.45;
    sound.currentTime = 0;

    sound.play().catch(() => {
      console.log(
        "Browser blocked autoplay audio."
      );
    });

  } catch {
    console.log(
      "Shutter sound unavailable."
    );
  }
}


/* ============================================================
   CAMERA INTRO
============================================================ */

function CameraIntro({ onComplete }) {

  useEffect(() => {

    const shutterTimer = setTimeout(() => {
      playShutterSound();
    }, 2450);


    const completeTimer = setTimeout(() => {
      onComplete();
    }, 3900);


    return () => {

      clearTimeout(
        shutterTimer
      );

      clearTimeout(
        completeTimer
      );

    };

  }, [onComplete]);


  return (
    <div className="camera-intro">

      <div className="intro-vignette" />


      <div className="camera-scene">

        <div className="camera-body">

          <div className="camera-top-strip">

            <span>
              MUVEFIT
            </span>

            <span>
              35 MM
            </span>

          </div>


          <div className="camera-body-details">

            <div className="camera-button" />

            <div className="camera-display">
              PHOTO
            </div>

          </div>


          <div className="lens-assembly">

            <div
              className="lens-metal-ring ring-one"
            />

            <div
              className="lens-metal-ring ring-two"
            />

            <div
              className="lens-metal-ring ring-three"
            />


            <div className="lens-glass">

              <div
                className="glass-reflection reflection-one"
              />

              <div
                className="glass-reflection reflection-two"
              />


              <div className="aperture">

                <div
                  className="aperture-blade blade-1"
                />

                <div
                  className="aperture-blade blade-2"
                />

                <div
                  className="aperture-blade blade-3"
                />

                <div
                  className="aperture-blade blade-4"
                />

                <div
                  className="aperture-blade blade-5"
                />

                <div
                  className="aperture-blade blade-6"
                />

                <div
                  className="aperture-center"
                />

              </div>

            </div>

          </div>

        </div>

      </div>


      <div className="camera-flash" />


      <div className="intro-brand">

        <div className="intro-brand-main">
          MuveFit
        </div>

        <div className="intro-brand-sub">
          MOVEMENT · FORM · BODY CARE
        </div>

      </div>

    </div>
  );
}


/* ============================================================
   CONSTELLATION FIELD
============================================================ */

function ConstellationField() {

  const points = [

    [2, 17],
    [9, 30],
    [18, 13],
    [27, 34],
    [37, 18],
    [46, 29],

    [56, 15],
    [65, 34],
    [75, 19],
    [84, 30],
    [94, 13],

    [7, 72],
    [17, 84],
    [29, 67],
    [40, 82],
    [53, 69],
    [65, 85],
    [78, 68],
    [91, 82]

  ];


  const lines = [

    [0, 1],
    [1, 2],
    [2, 3],
    [3, 4],
    [4, 5],

    [5, 6],
    [6, 7],
    [7, 8],
    [8, 9],
    [9, 10],

    [11, 12],
    [12, 13],
    [13, 14],
    [14, 15],
    [15, 16],
    [16, 17],
    [17, 18],

    [3, 13],
    [6, 15]

  ];


  return (
    <div className="constellation-field">

      {lines.map(([a, b], index) => {

        const start =
          points[a];

        const end =
          points[b];


        const dx =
          end[0] - start[0];

        const dy =
          end[1] - start[1];


        const distance =
          Math.sqrt(
            dx * dx +
            dy * dy
          );


        const angle =
          Math.atan2(
            dy,
            dx
          ) *
          180 /
          Math.PI;


        return (
          <span

            key={
              `constellation-line-${index}`
            }

            className="constellation-line"

            style={{
              left:
                `${start[0]}%`,

              top:
                `${start[1]}%`,

              width:
                `${distance}%`,

              transform:
                `rotate(${angle}deg)`
            }}

          />
        );

      })}


      {points.map(
        ([x, y], index) => (

          <span

            key={
              `constellation-point-${index}`
            }

            className="constellation-point"

            style={{
              left:
                `${x}%`,

              top:
                `${y}%`,

              animationDelay:
                `${index * 0.18}s`
            }}

          />

        )
      )}

    </div>
  );
}


/* ============================================================
   FITNESS CONSTELLATION
============================================================ */

function FitnessConstellation() {

  const points = [

    [12, 19],
    [24, 9],
    [37, 18],
    [48, 11],

    [61, 13],
    [76, 20],
    [89, 11],

    [9, 68],
    [22, 80],
    [36, 70],
    [51, 84],

    [66, 69],
    [81, 80],
    [94, 67]

  ];


  const links = [

    [0, 1],
    [1, 2],
    [2, 3],

    [4, 5],
    [5, 6],

    [7, 8],
    [8, 9],
    [9, 10],

    [10, 11],
    [11, 12],
    [12, 13],

    [2, 9],
    [5, 11]

  ];


  return (
    <div className="fitness-constellation">

      {links.map(
        ([a, b], index) => {

          const start =
            points[a];

          const end =
            points[b];


          const dx =
            end[0] - start[0];

          const dy =
            end[1] - start[1];


          const distance =
            Math.sqrt(
              dx * dx +
              dy * dy
            );


          const angle =
            Math.atan2(
              dy,
              dx
            ) *
            180 /
            Math.PI;


          return (
            <span

              key={
                `fitness-line-${index}`
              }

              className="fitness-line"

              style={{
                left:
                  `${start[0]}%`,

                top:
                  `${start[1]}%`,

                width:
                  `${distance}%`,

                transform:
                  `rotate(${angle}deg)`
              }}

            />
          );

        }
      )}


      {points.map(
        ([x, y], index) => (

          <span

            key={
              `fitness-dot-${index}`
            }

            className="fitness-dot"

            style={{
              left:
                `${x}%`,

              top:
                `${y}%`,

              animationDelay:
                `${index * 0.22}s`
            }}

          />

        )
      )}

    </div>
  );
}


/* ============================================================
   LANDING PAGE
============================================================ */

function Landing({
  onLogin,
  onSignup
}) {

  return (
    <div className="landing-page">

      <ConstellationField />


      {/* NAVBAR */}

      <nav className="landing-nav">

        <div className="brand">

          Muve<span>
            Fit
          </span>

        </div>


        <div className="nav-buttons">

          <button
            className="nav-login"
            onClick={onLogin}
          >
            Log in
          </button>


          <button
            className="nav-signup"
            onClick={onSignup}
          >
            Create account
          </button>

        </div>

      </nav>


      {/* HERO */}

      <main className="landing-hero">


        {/* LEFT */}

        <section className="hero-left">

          <div className="hero-eyebrow">

            <span className="status-dot" />

            CAMERA-BASED MOVEMENT ANALYSIS

          </div>


          <h1>

            Understand
            <br />

            how you{" "}

            <em>
              move.
            </em>

          </h1>


          <p>

            MuveFit uses your camera to understand
            movement, evaluate exercise form and
            help you become more aware of your body.

          </p>


          <div className="hero-buttons">

            <button
              className="primary-button"
              onClick={onSignup}
            >

              Start moving

              <span>
                →
              </span>

            </button>


            <button
              className="secondary-button"
              onClick={() =>
                document
                  .getElementById("how")
                  ?.scrollIntoView({
                    behavior:
                      "smooth"
                  })
              }
            >

              See how it works

            </button>

          </div>


          <div className="privacy-note">

            <div className="privacy-circle">
              +
            </div>


            <div>

              <strong>
                Movement stays private.
              </strong>

              <p>
                Workout videos are not permanently
                stored by default.
              </p>

            </div>

          </div>

        </section>


        {/* RIGHT */}

        <section className="hero-right">

          <FitnessConstellation />

          <div className="fitness-glow" />

          <div className="environment-ring ring-large" />

          <div className="environment-ring ring-medium" />

          <div className="environment-ring ring-small" />


          {/* REAL MAT */}

          <img
            src="/images/workout-mat.png"
            alt=""
            className="real-mat"
          />


          {/* REAL DUMBBELL */}

          <img
            src="/images/dumbbell.png"
            alt=""
            className="real-dumbbell"
          />


          <div className="fitness-data fitness-data-top">

            <span className="data-dot" />

            MOVEMENT READY

          </div>


          <div className="fitness-data fitness-data-bottom">

            <small>
              FORM SCORE
            </small>

            <strong>
              87%
            </strong>

            <span>
              good consistency
            </span>

          </div>

        </section>

      </main>


      {/* FEATURES */}

      <section className="feature-strip">

        <div>

          <small>
            01
          </small>

          <h3>
            Movement
          </h3>

          <p>
            Understand how your body moves.
          </p>

        </div>


        <div>

          <small>
            02
          </small>

          <h3>
            Form
          </h3>

          <p>
            Detect posture and movement accuracy.
          </p>

        </div>


        <div>

          <small>
            03
          </small>

          <h3>
            Body care
          </h3>

          <p>
            Exercise with greater awareness.
          </p>

        </div>


        <div>

          <small>
            04
          </small>

          <h3>
            Privacy
          </h3>

          <p>
            Your workout recordings stay private.
          </p>

        </div>

      </section>


      {/* HOW IT WORKS */}

      <section
        id="how"
        className="how-section"
      >

        <div className="how-heading">

          <small>
            HOW IT WORKS
          </small>

          <h2>

            A camera.
            <br />

            A movement.
            <br />

            A little more awareness.

          </h2>

        </div>


        <div className="how-grid">

          <article>

            <span>
              01
            </span>

            <h3>
              Choose
            </h3>

            <p>
              Select an exercise to analyse.
            </p>

          </article>


          <article>

            <span>
              02
            </span>

            <h3>
              Move
            </h3>

            <p>
              Use your camera while MuveFit
              observes your movement.
            </p>

          </article>


          <article>

            <span>
              03
            </span>

            <h3>
              Understand
            </h3>

            <p>
              See your form and movement insights.
            </p>

          </article>


          <article>

            <span>
              04
            </span>

            <h3>
              Improve
            </h3>

            <p>
              Track your movement over time.
            </p>

          </article>

        </div>

      </section>


      <footer className="footer">

        <strong>
          MuveFit
        </strong>

        <span>
          MOVEMENT · FORM · BODY CARE
        </span>

        <span>
          2026
        </span>

      </footer>

    </div>
  );
}


/* ============================================================
   AUTH
============================================================ */

function Auth({
  type,
  onBack,
  onSuccess
}) {

  const login =
    type === "login";


  return (
    <div className="auth-page">

      <ConstellationField />


      <button
        className="auth-back"
        onClick={onBack}
      >
        ← Back
      </button>


      <div className="auth-card">

        <div className="brand">

          Muve<span>
            Fit
          </span>

        </div>


        <small className="auth-label">

          {login
            ? "WELCOME BACK"
            : "CREATE YOUR ACCOUNT"}

        </small>


        <h1>

          {login
            ? "Good to see you."
            : "Let's get moving."}

        </h1>


        <p>

          {login
            ? "Sign in to continue your movement journey."
            : "Create your MuveFit account and start exploring your movement."}

        </p>


        {!login && (

          <label>

            Name

            <input
              type="text"
              placeholder="Your name"
            />

          </label>

        )}


        <label>

          Email

          <input
            type="email"
            placeholder="you@example.com"
          />

        </label>


        <label>

          Password

          <input
            type="password"
            placeholder="••••••••"
          />

        </label>


        <button
          className="auth-submit"
          onClick={onSuccess}
        >

          {login
            ? "Log in"
            : "Create account"}

          <span>
            →
          </span>

        </button>

      </div>

    </div>
  );
}


/* ============================================================
   APP NAVBAR
============================================================ */

function AppNav({
  onDashboard,
  onWorkout,
  onHistory,
  onProfile,
  onSafety
}) {

  return (
    <header className="app-nav">

      <button
        className="app-brand"
        onClick={onDashboard}
      >

        Muve<span>
          Fit
        </span>

      </button>


      <nav>

        <button
          onClick={onDashboard}
        >
          Dashboard
        </button>


        <button
          onClick={onWorkout}
        >
          Workout
        </button>


        <button
          onClick={onHistory}
        >
          History
        </button>


        <button
          onClick={onSafety}
        >
          Safety
        </button>


        <button
          onClick={onProfile}
        >
          Profile
        </button>

      </nav>

    </header>
  );
}


/* ============================================================
   DASHBOARD SIDEBAR
============================================================ */

function Sidebar({
  activePage,
  onDashboard,
  onWorkout,
  onHistory,
  onSafety,
  onProfile
}) {

  return (
    <aside className="dashboard-sidebar">

      <div>

        <div className="sidebar-label">
          YOUR SPACE
        </div>


        <button
          className={
            `sidebar-item ${
              activePage === "dashboard"
                ? "active"
                : ""
            }`
          }
          onClick={onDashboard}
        >

          <span>
            ◇
          </span>

          Dashboard

        </button>


        <button
          className={
            `sidebar-item ${
              activePage === "workout"
                ? "active"
                : ""
            }`
          }
          onClick={onWorkout}
        >

          <span>
            +
          </span>

          Start workout

        </button>


        <button
          className={
            `sidebar-item ${
              activePage === "history"
                ? "active"
                : ""
            }`
          }
          onClick={onHistory}
        >

          <span>
            ↗
          </span>

          History

        </button>


        <button
          className={
            `sidebar-item ${
              activePage === "safety"
                ? "active"
                : ""
            }`
          }
          onClick={onSafety}
        >

          <span>
            +
          </span>

          AI Safety

        </button>


        <button
          className={
            `sidebar-item ${
              activePage === "profile"
                ? "active"
                : ""
            }`
          }
          onClick={onProfile}
        >

          <span>
            ○
          </span>

          Profile

        </button>

      </div>


      <div className="sidebar-bottom">

        <div className="sidebar-privacy">

          <div className="privacy-symbol">
            +
          </div>

          <div>

            <strong>
              Privacy first
            </strong>

            <p>
              Videos aren't stored by default.
            </p>

          </div>

        </div>


        <button className="sidebar-settings">
          Settings
        </button>

      </div>

    </aside>
  );
}


/* ============================================================
   SCORE CARD
============================================================ */

function ScoreCard() {

  return (
    <section className="score-card">

      <div className="score-card-heading">

        <div>

          <span>
            YOUR MOVEMENT
          </span>

          <h2>
            Today's overview
          </h2>

        </div>


        <div className="score-live">
          LIVE DATA
        </div>

      </div>


      <div className="score-grid">

        <div className="score-item">

          <small>
            FORM SCORE
          </small>

          <strong>
            91%
          </strong>

          <span>
            +6% this week
          </span>

        </div>


        <div className="score-item">

          <small>
            ACCURACY
          </small>

          <strong>
            94%
          </strong>

          <span>
            movement consistency
          </span>

        </div>


        <div className="score-item">

          <small>
            WORKOUTS
          </small>

          <strong>
            24
          </strong>

          <span>
            total sessions
          </span>

        </div>


        <div className="score-item">

          <small>
            STREAK
          </small>

          <strong>
            6
          </strong>

          <span>
            days active
          </span>

        </div>

      </div>

    </section>
  );
}


/* ============================================================
   MOTIVATION SLIDER
============================================================ */

function MotivationSlider() {

  const slides = [

    {
      title:
        "Consistency beats intensity.",

      text:
        "Small improvements in form add up."
    },

    {
      title:
        "Your movement is improving.",

      text:
        "Your form score is up 6% this week."
    },

    {
      title:
        "Focus on the next rep.",

      text:
        "Quality reps matter more than rushing."
    },

    {
      title:
        "Move with intention.",

      text:
        "Good movement starts with awareness."
    }

  ];


  const [active, setActive] =
    useState(0);


  useEffect(() => {

    const timer =
      setInterval(() => {

        setActive(
          previous =>
            (
              previous + 1
            ) %
            slides.length
        );

      }, 4500);


    return () => {
      clearInterval(timer);
    };

  }, [slides.length]);


  return (
    <section className="motivation-slider">

      <div className="motivation-orbit" />


      <div className="motivation-content">

        <span className="motivation-label">

          MOVE NOTE /{" "}

          {
            String(
              active + 1
            ).padStart(
              2,
              "0"
            )
          }

        </span>


        <h2>
          {slides[active].title}
        </h2>


        <p>
          {slides[active].text}
        </p>


        <div className="motivation-dots">

          {slides.map(
            (_, index) => (

              <button

                key={index}

                className={
                  index === active
                    ? "active"
                    : ""
                }

                onClick={() =>
                  setActive(index)
                }

              />

            )
          )}

        </div>

      </div>

    </section>
  );
}


/* ============================================================
   SKELETON PREVIEW
============================================================ */

function SkeletonPreview() {

  return (
    <section className="skeleton-preview">

      <div className="skeleton-header">

        <div>

          <span>
            MOVEMENT SENSOR
          </span>

          <h2>
            Your movement space
          </h2>

        </div>


        <div className="sensor-status">

          <span />

          READY

        </div>

      </div>


      <div className="skeleton-stage">

        {/* SENSOR NODES */}

        <span className="sensor-node node-1" />
        <span className="sensor-node node-2" />
        <span className="sensor-node node-3" />
        <span className="sensor-node node-4" />
        <span className="sensor-node node-5" />
        <span className="sensor-node node-6" />
        <span className="sensor-node node-7" />
        <span className="sensor-node node-8" />


        {/* SENSOR LINES */}

        <span className="sensor-line sensor-line-1" />
        <span className="sensor-line sensor-line-2" />
        <span className="sensor-line sensor-line-3" />
        <span className="sensor-line sensor-line-4" />
        <span className="sensor-line sensor-line-5" />


        {/* HEAD */}

        <div className="skeleton-head" />


        {/* SPINE */}

        <div className="skeleton-spine" />


        {/* SHOULDERS */}

        <div className="skeleton-shoulder" />


        {/* HIPS */}

        <div className="skeleton-hip" />


        {/* LEFT ARM */}

        <div className="skeleton-arm arm-left-upper" />
        <div className="skeleton-arm arm-left-lower" />


        {/* RIGHT ARM */}

        <div className="skeleton-arm arm-right-upper" />
        <div className="skeleton-arm arm-right-lower" />


        {/* LEFT LEG */}

        <div className="skeleton-leg leg-left-upper" />
        <div className="skeleton-leg leg-left-lower" />


        {/* RIGHT LEG */}

        <div className="skeleton-leg leg-right-upper" />
        <div className="skeleton-leg leg-right-lower" />


        {/* JOINTS */}

        <span className="joint head-joint" />

        <span className="joint shoulder-left" />
        <span className="joint shoulder-right" />

        <span className="joint elbow-left" />
        <span className="joint elbow-right" />

        <span className="joint wrist-left" />
        <span className="joint wrist-right" />

        <span className="joint hip-left" />
        <span className="joint hip-right" />

        <span className="joint knee-left" />
        <span className="joint knee-right" />

        <span className="joint ankle-left" />
        <span className="joint ankle-right" />


        <div className="skeleton-message">
          SELECT AN EXERCISE TO BEGIN
        </div>

      </div>


      <div className="skeleton-footer">

        <span>
          CAMERA
        </span>

        <span>
          •
        </span>

        <span>
          POSE LANDMARKS
        </span>

        <span>
          •
        </span>

        <span>
          REAL-TIME
        </span>

      </div>

    </section>
  );
}


/* ============================================================
   DASHBOARD
============================================================ */

function Dashboard({
  onDashboard,
  onWorkout,
  onHistory,
  onSafety,
  onProfile
}) {

  return (
    <div className="dashboard-shell">


      <AppNav

        onDashboard={
          onDashboard
        }

        onWorkout={
          onWorkout
        }

        onHistory={
          onHistory
        }

        onSafety={
          onSafety
        }

        onProfile={
          onProfile
        }

      />


      <div className="dashboard-layout">


        <Sidebar

          activePage="dashboard"

          onDashboard={
            onDashboard
          }

          onWorkout={
            onWorkout
          }

          onHistory={
            onHistory
          }

          onSafety={
            onSafety
          }

          onProfile={
            onProfile
          }

        />


        <main className="dashboard-main">


          {/* WELCOME */}

          <section className="dashboard-welcome">

            <div>

              <span className="dashboard-label">
                DASHBOARD / TODAY
              </span>

              <h1>
                Good evening.
              </h1>

              <p>
                Ready to check in with your movement?
              </p>

            </div>


            <button

              className="dashboard-start-button"

              onClick={onWorkout}

            >

              Start workout

              <span>
                →
              </span>

            </button>

          </section>


          {/* SCORECARD */}

          <ScoreCard />


          {/* MOTIVATION */}

          <MotivationSlider />


          {/* SKELETON */}

          <SkeletonPreview />


          {/* QUICK ACTIONS */}

          <section className="dashboard-quick-actions">

            <button
              onClick={onWorkout}
            >
              <span>+</span>
              New workout
              <strong>→</strong>
            </button>


            <button
              onClick={onHistory}
            >
              <span>↗</span>
              View reports
              <strong>→</strong>
            </button>


            <button
              onClick={onSafety}
            >
              <span>+</span>
              AI safety check
              <strong>→</strong>
            </button>

          </section>

        </main>

      </div>

    </div>
  );
}


/* ============================================================
   WORKOUT SELECTION
============================================================ */

function WorkoutSelection({
  onBack,
  onStart
}) {

  const exercises = [

    {
      id: "squat",
      name: "Squat",
      description:
        "Depth · knees · torso",
      metric: "REPS"
    },

    {
      id: "plank",
      name: "Plank",
      description:
        "Alignment · stability",
      metric: "TIME"
    },

    {
      id: "burpee",
      name: "Burpee",
      description:
        "Jump · landing · rhythm",
      metric: "REPS"
    },

    {
      id: "squat-hold",
      name: "Squat Hold",
      description:
        "Depth · stability · duration",
      metric: "TIME"
    },

    {
      id: "glute-bridge",
      name: "Glute Bridge",
      description:
        "Hip · alignment · control",
      metric: "REPS"
    }

  ];


  return (
    <div className="app-page">

      <AppBack
        onClick={onBack}
      />


      <main className="workout-select">

        <span className="section-label">
          WORKOUT
        </span>


        <h1>
          Choose your
          <br />
          <em>movement.</em>
        </h1>


        <p>
          Select an exercise and let the camera
          analyse your form.
        </p>


        <div className="exercise-grid">

          {exercises.map(
            (exercise, index) => (

              <button

                key={
                  exercise.id
                }

                className={
                  `exercise-card exercise-${index + 1}`
                }

                onClick={() =>
                  onStart(
                    exercise.id
                  )
                }

              >

                <span className="exercise-number">
                  0{index + 1}
                </span>


                <h3>
                  {exercise.name}
                </h3>


                <p>
                  {exercise.description}
                </p>


                <span className="exercise-metric">
                  {exercise.metric}
                </span>


                <span className="exercise-arrow">
                  →
                </span>

              </button>

            )
          )}

        </div>

      </main>

    </div>
  );
}


/* ============================================================
   WORKOUT SCREEN
============================================================ */

function WorkoutScreen({
  exercise,
  onBack,
  onFinish
}) {

  const names = {

    squat:
      "SQUAT",

    plank:
      "PLANK",

    burpee:
      "BURPEE",

    "squat-hold":
      "SQUAT HOLD",

    "glute-bridge":
      "GLUTE BRIDGE"

  };


  return (
    <div className="workout-screen">


      <header className="workout-top">

        <button
          onClick={onBack}
        >
          ←
        </button>


        <span>
          {names[exercise]}
        </span>


        <span>
          CAMERA
        </span>

      </header>


      <main className="camera-area">

        <div className="camera-frame">


          <span className="corner top-left" />

          <span className="corner top-right" />

          <span className="corner bottom-left" />

          <span className="corner bottom-right" />


          <div className="demo-skeleton">

            <span className="demo-head" />

            <span className="demo-body" />

            <span className="demo-arm left" />

            <span className="demo-arm right" />

            <span className="demo-leg left" />

            <span className="demo-leg right" />

          </div>


          <div className="camera-feed-label">
            CAMERA FEED
          </div>


          <div className="live-badge">

            <span />

            LIVE ANALYSIS

          </div>

        </div>

      </main>


      <footer className="workout-bottom">


        <div className="workout-stat">

          <small>
            REP
          </small>

          <strong>
            08
          </strong>

        </div>


        <div className="workout-stat accuracy">

          <small>
            ACCURACY
          </small>

          <strong>
            91%
          </strong>

        </div>


        <div className="workout-form">

          <small>
            FORM
          </small>

          <strong>
            GOOD FORM
          </strong>

        </div>


        <button
          className="finish-workout"
          onClick={onFinish}
        >
          END
        </button>

      </footer>

    </div>
  );
}


/* ============================================================
   HISTORY
============================================================ */

function History({
  onBack
}) {

  const reports = [

    {
      date:
        "02 SEP 2026",

      exercise:
        "Squat",

      reps:
        "12 reps",

      score:
        "91%",

      rating:
        "Excellent"
    },

    {
      date:
        "01 SEP 2026",

      exercise:
        "Plank",

      reps:
        "42 sec",

      score:
        "88%",

      rating:
        "Good"
    },

    {
      date:
        "30 AUG 2026",

      exercise:
        "Glute Bridge",

      reps:
        "15 reps",

      score:
        "94%",

      rating:
        "Excellent"
    }

  ];


  return (
    <div className="app-page">

      <AppBack
        onClick={onBack}
      />


      <main className="history-page">

        <span className="section-label">
          HISTORY / REPORTS
        </span>


        <h1>

          Your movement
          <br />

          <em>
            over time.
          </em>

        </h1>


        <div className="history-chart">

          <div className="history-score">
            91%
          </div>

          <span>
            FORM CONSISTENCY
          </span>


          <div className="history-bars">

            <i style={{ height: "45%" }} />

            <i style={{ height: "58%" }} />

            <i style={{ height: "51%" }} />

            <i style={{ height: "68%" }} />

            <i style={{ height: "73%" }} />

            <i style={{ height: "81%" }} />

            <i style={{ height: "91%" }} />

          </div>

        </div>


        <div className="reports-list">

          {reports.map(
            report => (

              <div
                key={
                  report.date
                }
                className="report-row"
              >

                <div className="report-date">
                  {report.date}
                </div>


                <div className="report-exercise">

                  <strong>
                    {report.exercise}
                  </strong>

                  <span>
                    {report.reps}
                  </span>

                </div>


                <div className="report-score">
                  {report.score}
                </div>


                <div className="report-rating">
                  {report.rating}
                </div>


                <button>
                  →
                </button>

              </div>

            )
          )}

        </div>

      </main>

    </div>
  );
}


/* ============================================================
   PROFILE
============================================================ */

function Profile({
  onBack
}) {

  return (
    <div className="app-page">

      <AppBack
        onClick={onBack}
      />


      <main className="profile-page">

        <span className="section-label">
          PROFILE
        </span>


        <div className="profile-header">

          <div className="profile-avatar">
            MF
          </div>


          <div>

            <h1>
              Your profile
            </h1>

            <p>
              Movement journey
            </p>

          </div>

        </div>


        <div className="profile-grid">

          <div className="profile-item">

            <small>
              NAME
            </small>

            <strong>
              Your Name
            </strong>

          </div>


          <div className="profile-item">

            <small>
              EMAIL
            </small>

            <strong>
              you@example.com
            </strong>

          </div>


          <div className="profile-item">

            <small>
              WORKOUTS
            </small>

            <strong>
              24
            </strong>

          </div>


          <div className="profile-item">

            <small>
              BEST FORM
            </small>

            <strong>
              96%
            </strong>

          </div>

        </div>


        <div className="profile-privacy">

          <span>
            PRIVACY
          </span>


          <strong>
            Workout videos are not stored by default.
          </strong>


          <p>
            Analysis results can be retained for your
            movement history.
          </p>

        </div>

      </main>

    </div>
  );
}


/* ============================================================
   SAFETY
============================================================ */

function Safety({
  onBack
}) {

  const [message, setMessage] =
    useState("");


  return (
    <div className="app-page">

      <AppBack
        onClick={onBack}
      />


      <main className="safety-page">

        <span className="section-label">
          AI SAFETY / BODY CHECK
        </span>


        <h1>

          Something feel
          <br />

          <em>
            different?
          </em>

        </h1>


        <p>

          Tell MuveFit what you're experiencing.
          This section can later connect to your
          embedded safety chatbot.

        </p>


        <textarea

          value={message}

          onChange={
            event =>
              setMessage(
                event.target.value
              )
          }

          placeholder="Describe discomfort, pain, fatigue or another symptom..."

        />


        <button className="safety-submit">
          Start safety check →
        </button>


        <div className="safety-warning">

          <strong>
            IMPORTANT
          </strong>

          <span>

            MuveFit is not a medical diagnosis tool.
            Seek professional care for urgent or serious
            symptoms.

          </span>

        </div>

      </main>

    </div>
  );
}


/* ============================================================
   BACK BUTTON
============================================================ */

function AppBack({
  onClick
}) {

  return (
    <button
      className="app-back"
      onClick={onClick}
    >
      ← Back
    </button>
  );
}


/* ============================================================
   APP
============================================================ */

function App() {

  const [
    showIntro,
    setShowIntro
  ] = useState(true);


  const [
    screen,
    setScreen
  ] = useState("landing");


  const [
    selectedExercise,
    setSelectedExercise
  ] = useState(null);


  /* ========================================================
     INTRO
  ======================================================== */

  if (showIntro) {

    return (
      <CameraIntro

        onComplete={() =>
          setShowIntro(false)
        }

      />
    );
  }


  /* ========================================================
     LANDING
  ======================================================== */

  if (
    screen === "landing"
  ) {

    return (
      <Landing

        onLogin={() =>
          setScreen("login")
        }

        onSignup={() =>
          setScreen("signup")
        }

      />
    );
  }


  /* ========================================================
     LOGIN
  ======================================================== */

  if (
    screen === "login"
  ) {

    return (
      <Auth

        type="login"

        onBack={() =>
          setScreen("landing")
        }

        onSuccess={() =>
          setScreen("dashboard")
        }

      />
    );
  }


  /* ========================================================
     SIGNUP
  ======================================================== */

  if (
    screen === "signup"
  ) {

    return (
      <Auth

        type="signup"

        onBack={() =>
          setScreen("landing")
        }

        onSuccess={() =>
          setScreen("dashboard")
        }

      />
    );
  }


  /* ========================================================
     DASHBOARD
  ======================================================== */

  if (
    screen === "dashboard"
  ) {

    return (
      <Dashboard

        onDashboard={() =>
          setScreen("dashboard")
        }

        onWorkout={() =>
          setScreen("workout-select")
        }

        onHistory={() =>
          setScreen("history")
        }

        onSafety={() =>
          setScreen("safety")
        }

        onProfile={() =>
          setScreen("profile")
        }

      />
    );
  }


  /* ========================================================
     WORKOUT SELECTION
  ======================================================== */

  if (
    screen === "workout-select"
  ) {

    return (
      <WorkoutSelection

        onBack={() =>
          setScreen("dashboard")
        }

        onStart={
          exercise => {

            setSelectedExercise(
              exercise
            );

            setScreen(
              "workout"
            );

          }
        }

      />
    );
  }


  /* ========================================================
     WORKOUT CAMERA
  ======================================================== */

  if (
    screen === "workout"
  ) {

    return (
      <WorkoutScreen

        exercise={
          selectedExercise
        }

        onBack={() =>
          setScreen("workout-select")
        }

        onFinish={() =>
          setScreen("history")
        }

      />
    );
  }


  /* ========================================================
     HISTORY
  ======================================================== */

  if (
    screen === "history"
  ) {

    return (
      <History

        onBack={() =>
          setScreen("dashboard")
        }

      />
    );
  }


  /* ========================================================
     PROFILE
  ======================================================== */

  if (
    screen === "profile"
  ) {

    return (
      <Profile

        onBack={() =>
          setScreen("dashboard")
        }

      />
    );
  }


  /* ========================================================
     SAFETY
  ======================================================== */

  if (
    screen === "safety"
  ) {

    return (
      <Safety

        onBack={() =>
          setScreen("dashboard")
        }

      />
    );
  }


  return null;
}


export default App;