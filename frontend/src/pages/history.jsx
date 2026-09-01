import { Link } from "react-router-dom";

function History() {
  return (
    <div className="page" style={{ padding: 40 }}>
      <div className="container">

        <Link to="/dashboard">
          ← Dashboard
        </Link>

        <h1 style={{ marginTop: 30 }}>
          Workout History
        </h1>

        <div
          className="card"
          style={{
            marginTop: 25,
            padding: 30
          }}
        >
          Squat — 87% — 12 reps
        </div>

      </div>
    </div>
  );
}

export default History;