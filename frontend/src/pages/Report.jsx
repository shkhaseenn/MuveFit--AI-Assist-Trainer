import { Link } from "react-router-dom";

function Report() {
  return (
    <div className="page" style={{ padding: 40 }}>
      <div className="container">

        <Link to="/history">
          ← History
        </Link>

        <h1 style={{ marginTop: 30 }}>
          Exercise Report
        </h1>

        <div
          className="card"
          style={{
            marginTop: 25,
            padding: 30
          }}
        >
          <h2>87%</h2>

          <p>
            Form Accuracy
          </p>

          <br />

          <p>
            Depth: 92%
          </p>

          <p>
            Alignment: 84%
          </p>

          <p>
            Torso: 85%
          </p>

        </div>

      </div>
    </div>
  );
}

export default Report;