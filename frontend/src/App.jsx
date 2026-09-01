import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [intro, setIntro] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIntro(false);
    }, 3200);

    return () => clearTimeout(timer);
  }, []);

  if (intro) {
    return (
      <div className="intro-screen">
        <div className="intro-content">

          <div className="racer">
            <span></span>
            <span></span>
            <span></span>
          </div>

          <h1 className="intro-logo">
            MuveFit
          </h1>

          <p className="intro-tagline">
            MOVE BETTER
          </p>

        </div>
      </div>
    );
  }

  return (
    <div className="landing">

      {/* Decorative shapes */}
      <div className="blob blob-one"></div>
      <div className="blob blob-two"></div>

      <nav className="navbar">
        <div className="brand">
          Muve<span>Fit</span>
        </div>

        <div className="nav-right">
          <button
            className="nav-login"
            onClick={() => alert("Login page coming next")}
          >
            Login
          </button>

          <button
            className="nav-signup"
            onClick={() => alert("Create account page coming next")}
          >
            Get started
          </button>
        </div>
      </nav>

      <main className="hero-section">

        <div className="hero-copy">

          <div className="pill">
            <span className="pulse"></span>
            AI MOVEMENT ANALYSIS
          </div>

          <h1>
            Move smarter.
            <br />
            <span>Feel stronger.</span>
          </h1>

          <p>
            Your personal AI movement coach.
            Track your exercises, understand your
            form, and train with more confidence.
          </p>

          <div className="hero-buttons">

            <button
              className="main-button"
              onClick={() => alert("Create account page coming next")}
            >
              Create account
              <span>→</span>
            </button>

            <button
              className="outline-button"
              onClick={() => alert("Login page coming next")}
            >
              I already have an account
            </button>

          </div>

          <div className="trust-row">
            <div>
              <strong>AI</strong>
              <span>Pose tracking</span>
            </div>

            <div>
              <strong>100%</strong>
              <span>Private sessions</span>
            </div>

            <div>
              <strong>4+</strong>
              <span>Exercises</span>
            </div>
          </div>

        </div>

        <div className="hero-visual">

          <div className="visual-card">

            <div className="visual-top">
              <span>LIVE ANALYSIS</span>
              <span className="live-dot"></span>
            </div>

            <div className="skeleton-area">

              <div className="person-head"></div>

              <div className="body-line body-main"></div>

              <div className="body-line arm-left"></div>
              <div className="body-line arm-right"></div>

              <div className="body-line leg-left"></div>
              <div className="body-line leg-right"></div>

              <div className="joint j1"></div>
              <div className="joint j2"></div>
              <div className="joint j3"></div>
              <div className="joint j4"></div>
              <div className="joint j5"></div>
              <div className="joint j6"></div>

            </div>

            <div className="analysis-card">

              <div>
                <small>FORM ACCURACY</small>
                <strong>94%</strong>
              </div>

              <div className="score-ring">
                <span>✓</span>
              </div>

            </div>

          </div>

          <div className="floating-card card-top">
            <span>✦</span>
            Good alignment
          </div>

          <div className="floating-card card-bottom">
            <strong>12</strong>
            <span>reps analysed</span>
          </div>

        </div>

      </main>

      <section className="privacy-section">

        <div className="privacy-icon">
          ✓
        </div>

        <div>
          <strong>Your movement stays private.</strong>
          <p>
            Exercise recordings are not stored.
            MuveFit focuses on analysis, not collecting
            your personal videos.
          </p>
        </div>

      </section>

    </div>
  );
}

export default App;