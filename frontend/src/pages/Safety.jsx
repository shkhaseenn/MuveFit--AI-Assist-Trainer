import { Link } from "react-router-dom";

function Safety() {
  return (
    <div className="page" style={{ padding: 40 }}>
      <div className="container">

        <Link to="/dashboard">
          ← Dashboard
        </Link>

        <h1 style={{ marginTop: 30 }}>
          Safety
        </h1>

        <div
          className="card"
          style={{
            marginTop: 25,
            padding: 30
          }}
        >

          <h2>
            How are you feeling?
          </h2>

          <p
            className="muted"
            style={{
              marginTop: 10
            }}
          >
            Safety and symptom analysis will be
            connected here.
          </p>

        </div>

      </div>
    </div>
  );
}

export default Safety;