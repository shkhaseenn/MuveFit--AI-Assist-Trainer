import { Link } from "react-router-dom";
import {
  Home,
  Dumbbell,
  ShieldCheck,
  History as HistoryIcon,
  User
} from "lucide-react";

import "../App.css";

const exercises = [
  {
    name: "Squat",
    description: "Depth + alignment"
  },
  {
    name: "Plank",
    description: "Core alignment"
  },
  {
    name: "Burpee",
    description: "Full-body movement"
  },
  {
    name: "Squat Hold",
    description: "Strength + stability"
  },
  {
    name: "Glute Bridge",
    description: "Hip alignment"
  }
];

function Dashboard() {

  return (

    <div className="dashboard-layout">

      {/* DESKTOP SIDEBAR */}

      <aside className="sidebar">

        <div className="sidebar-logo">
          MuveFit
        </div>

        <nav className="sidebar-nav">

          <Link className="sidebar-link" to="/dashboard">
            <Home size={17} /> Home
          </Link>

          <Link className="sidebar-link" to="/workout">
            <Dumbbell size={17} /> Workout
          </Link>

          <Link className="sidebar-link" to="/safety">
            <ShieldCheck size={17} /> Safety
          </Link>

          <Link className="sidebar-link" to="/history">
            <HistoryIcon size={17} /> History
          </Link>

          <Link className="sidebar-link" to="/profile">
            <User size={17} /> Profile
          </Link>

        </nav>

      </aside>


      {/* MAIN */}

      <main className="dashboard-main">

        <div className="dashboard-top">

          <div>
            <p className="muted">
              Tuesday, September 1
            </p>

            <h1>
              Good evening 👋
            </h1>
          </div>

          <Link
            to="/profile"
            className="profile-button"
          >
            <User size={20} />
          </Link>

        </div>


        {/* HERO */}

        <section className="dashboard-hero">

          <div>

            <p
              style={{
                fontWeight: 700,
                marginBottom: 10
              }}
            >
              READY TO MOVE?
            </p>

            <h2>
              Your body knows the movement.
              Let's make it better.
            </h2>

          </div>

          <Link
            to="/workout"
            className="primary-button"
          >
            Start Fitness →
          </Link>

        </section>


        {/* STATS */}

        <section className="stats-grid">

          <div className="card stat-card">
            <div className="stat-value">
              87%
            </div>

            <div className="stat-label">
              Average Form
            </div>
          </div>


          <div className="card stat-card">
            <div className="stat-value">
              12
            </div>

            <div className="stat-label">
              Workouts
            </div>
          </div>


          <div className="card stat-card">
            <div className="stat-value">
              +8%
            </div>

            <div className="stat-label">
              Improvement
            </div>
          </div>

        </section>


        {/* EXERCISES */}

        <h2 className="section-title">
          Train with MuveFit
        </h2>

        <section className="exercise-grid">

          {exercises.map((exercise) => (

            <Link
              key={exercise.name}
              to={`/workout?exercise=${encodeURIComponent(exercise.name)}`}
              className="card exercise-card"
            >

              <div>
                <p className="muted">
                  AI ANALYSIS
                </p>

                <h3>
                  {exercise.name}
                </h3>
              </div>

              <p className="muted">
                {exercise.description}
              </p>

            </Link>

          ))}

        </section>


        {/* RECENT */}

        <h2 className="section-title">
          Recent activity
        </h2>

        <div
          className="card"
          style={{
            padding: 25
          }}
        >

          <strong>
            Squat
          </strong>

          <span
            style={{
              marginLeft: 20
            }}
          >
            87%
          </span>

          <span
            className="muted"
            style={{
              marginLeft: 20
            }}
          >
            12 reps
          </span>

        </div>

      </main>


      {/* MOBILE NAV */}

      <nav className="bottom-nav">

        <Link to="/dashboard">
          Home
        </Link>

        <Link to="/workout">
          Workout
        </Link>

        <Link to="/safety">
          Safety
        </Link>

        <Link to="/history">
          History
        </Link>

        <Link to="/profile">
          Profile
        </Link>

      </nav>

    </div>
  );
}

export default Dashboard;