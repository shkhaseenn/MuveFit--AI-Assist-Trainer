import React from "react";

function ScoreCard({
  formScore = 91,
  accuracy = 94,
  workouts = 24,
  streak = 6
}) {

  return (
    <section className="score-card">

      <div className="score-card-header">

        <div>

          <span>
            YOUR MOVEMENT
          </span>

          <h2>
            Today's overview
          </h2>

        </div>


        <div className="score-status">
          LIVE DATA
        </div>

      </div>


      <div className="score-card-grid">


        {/* FORM */}

        <div className="score-metric primary-score">

          <small>
            FORM SCORE
          </small>

          <strong>
            {formScore}%
          </strong>

          <span>
            +6% this week
          </span>

        </div>


        {/* ACCURACY */}

        <div className="score-metric">

          <small>
            ACCURACY
          </small>

          <strong>
            {accuracy}%
          </strong>

          <span>
            movement consistency
          </span>

        </div>


        {/* WORKOUTS */}

        <div className="score-metric">

          <small>
            WORKOUTS
          </small>

          <strong>
            {workouts}
          </strong>

          <span>
            total sessions
          </span>

        </div>


        {/* STREAK */}

        <div className="score-metric">

          <small>
            STREAK
          </small>

          <strong>
            {streak}
          </strong>

          <span>
            days active
          </span>

        </div>

      </div>

    </section>
  );
}

export default ScoreCard;