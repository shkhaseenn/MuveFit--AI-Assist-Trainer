import React from "react";

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

        {/* constellation */}

        <span className="sensor-node node-1" />
        <span className="sensor-node node-2" />
        <span className="sensor-node node-3" />
        <span className="sensor-node node-4" />
        <span className="sensor-node node-5" />
        <span className="sensor-node node-6" />
        <span className="sensor-node node-7" />
        <span className="sensor-node node-8" />


        <span className="sensor-line line-1" />
        <span className="sensor-line line-2" />
        <span className="sensor-line line-3" />
        <span className="sensor-line line-4" />
        <span className="sensor-line line-5" />
        <span className="sensor-line line-6" />


        {/* HEAD */}

        <div className="skeleton-head" />


        {/* BODY */}

        <div className="skeleton-spine" />

        <div className="skeleton-shoulder" />

        <div className="skeleton-hip" />


        {/* ARMS */}

        <div className="skeleton-arm arm-left-upper" />
        <div className="skeleton-arm arm-left-lower" />

        <div className="skeleton-arm arm-right-upper" />
        <div className="skeleton-arm arm-right-lower" />


        {/* LEGS */}

        <div className="skeleton-leg leg-left-upper" />
        <div className="skeleton-leg leg-left-lower" />

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

export default SkeletonPreview;