import React from "react";

import AppNav from "./AppNav";
import Sidebar from "./Sidebar";
import ScoreCard from "./ScoreCard";
import MotivationSlider from "./MotivationSlider";
import SkeletonPreview from "./SkeletonPreview";


function Dashboard({
  onDashboard,
  onWorkout,
  onHistory,
  onSafety,
  onProfile,
  onNotifications
}) {

  return (
    <div className="dashboard-shell">


      {/* ==================================================
          NAVBAR
      ================================================== */}

      <AppNav
        onProfile={onProfile}
        onNotifications={onNotifications}
      />


      <div className="dashboard-layout">


        {/* ==================================================
            SIDEBAR
        ================================================== */}

        <Sidebar

          activePage="dashboard"

          onDashboard={onDashboard}

          onWorkout={onWorkout}

          onHistory={onHistory}

          onSafety={onSafety}

          onProfile={onProfile}

        />


        {/* ==================================================
            MAIN
        ================================================== */}

        <main className="dashboard-main">


          {/* HEADER */}

          <section className="dashboard-welcome">

            <div>

              <span className="dashboard-label">
                DASHBOARD / 02 SEP 2026
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


          {/* ==================================================
              SCORE CARD
          ================================================== */}

          <ScoreCard
            formScore={91}
            accuracy={94}
            workouts={24}
            streak={6}
          />


          {/* ==================================================
              MOTIVATION
          ================================================== */}

          <MotivationSlider />


          {/* ==================================================
              SKELETON
          ================================================== */}

          <SkeletonPreview />


          {/* ==================================================
              QUICK LINKS
          ================================================== */}

          <section className="dashboard-quick-links">

            <button
              onClick={onWorkout}
              className="quick-link"
            >

              <span>
                + 
              </span>

              New workout

              <strong>
                →
              </strong>

            </button>


            <button
              onClick={onHistory}
              className="quick-link"
            >

              <span>
                ↗
              </span>

              View reports

              <strong>
                →
              </strong>

            </button>


            <button
              onClick={onSafety}
              className="quick-link"
            >

              <span>
                +
              </span>

              AI safety check

              <strong>
                →
              </strong>

            </button>

          </section>


        </main>

      </div>

    </div>
  );
}

export default Dashboard;