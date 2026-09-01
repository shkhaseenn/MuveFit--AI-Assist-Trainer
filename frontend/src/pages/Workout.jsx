import { Link, useSearchParams } from "react-router-dom";
import "../App.css";

function Workout() {

  const [searchParams] = useSearchParams();

  const exercise =
    searchParams.get("exercise") || "Squat";

  return (

    <div
      className="page"
      style={{
        padding: 30
      }}
    >

      <div className="container">

        <Link to="/dashboard">
          ← Dashboard
        </Link>


        <div
          style={{
            marginTop: 30,
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center"
          }}
        >

          <div>

            <p className="muted">
              AI WORKOUT
            </p>

            <h1>
              {exercise}
            </h1>

          </div>

          <strong>
            FORM 100%
          </strong>

        </div>


        <div
          className="card"
          style={{
            marginTop: 25,
            minHeight: "65vh",
            background: "#202124",
            color: "white",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexDirection: "column"
          }}
        >

          <div
            style={{
              fontSize: 80,
              opacity: 0.7
            }}
          >
            🧍
          </div>

          <h2>
            Camera / Skeleton Area
          </h2>

          <p
            style={{
              opacity: 0.6,
              marginTop: 10
            }}
          >
            MediaPipe will be connected here.
          </p>

        </div>


        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginTop: 20
          }}
        >

          <strong>
            REP 00
          </strong>

          <button className="primary-button">
            Start
          </button>

        </div>

      </div>

    </div>
  );
}

export default Workout;