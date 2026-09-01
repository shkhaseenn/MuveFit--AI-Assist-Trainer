import { Link } from "react-router-dom";

function Profile() {
  return (
    <div className="page" style={{ padding: 40 }}>
      <div className="container">

        <Link to="/dashboard">
          ← Dashboard
        </Link>

        <h1 style={{ marginTop: 30 }}>
          Profile
        </h1>

        <div
          className="card"
          style={{
            marginTop: 25,
            padding: 30
          }}
        >

          <h2>
            Your Profile
          </h2>

          <p style={{ marginTop: 15 }}>
            Name: Demo User
          </p>

          <p>
            Email: demo@example.com
          </p>

        </div>

      </div>
    </div>
  );
}

export default Profile;