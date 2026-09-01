import React from "react";

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

      <div className="sidebar-top">

        <div className="sidebar-section-label">
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

          <span className="sidebar-icon">
            ◇
          </span>

          <span>
            Dashboard
          </span>

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

          <span className="sidebar-icon">
            +
          </span>

          <span>
            Start workout
          </span>

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

          <span className="sidebar-icon">
            ↗
          </span>

          <span>
            History
          </span>

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

          <span className="sidebar-icon">
            +
          </span>

          <span>
            AI Safety
          </span>

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

          <span className="sidebar-icon">
            ○
          </span>

          <span>
            Profile
          </span>

        </button>

      </div>


      <div className="sidebar-bottom">

        <div className="sidebar-privacy">

          <span className="privacy-symbol">
            +
          </span>

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

export default Sidebar;