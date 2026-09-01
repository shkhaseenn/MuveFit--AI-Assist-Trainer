import React from "react";

function AppNav({
  onProfile,
  onNotifications
}) {
  return (
    <header className="app-navbar">

      <div className="app-navbar-left">

        <button
          className="mobile-menu-button"
          aria-label="Open menu"
        >
          ☰
        </button>

        <button
          className="app-navbar-brand"
          onClick={() => window.scrollTo({
            top: 0,
            behavior: "smooth"
          })}
        >
          Muve<span>Fit</span>
        </button>

      </div>


      <div className="app-navbar-right">

        <button
          className="notification-button"
          onClick={onNotifications}
          aria-label="Notifications"
        >
          <span className="notification-dot" />
          ◌
        </button>


        <button
          className="navbar-profile"
          onClick={onProfile}
        >

          <span className="navbar-avatar">
            MF
          </span>

          <span className="navbar-profile-text">
            Profile
          </span>

        </button>

      </div>

    </header>
  );
}

export default AppNav;