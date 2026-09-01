import { Link, useNavigate } from "react-router-dom";
import "../App.css";

function Login() {

  const navigate = useNavigate();

  function handleLogin(e) {
    e.preventDefault();

    // Temporary frontend login.
    // Backend authentication will replace this later.

    navigate("/dashboard");
  }

  return (
    <div className="auth-page">

      <div className="auth-card">

        <div className="logo">
          MuveFit
        </div>

        <h1 style={{ marginTop: 30 }}>
          Welcome back.
        </h1>

        <p className="muted">
          Continue your movement journey.
        </p>

        <form onSubmit={handleLogin}>

          <div className="form-group">
            <label>Email</label>

            <input
              type="email"
              placeholder="you@example.com"
              required
            />
          </div>


          <div className="form-group">
            <label>Password</label>

            <input
              type="password"
              placeholder="••••••••"
              required
            />
          </div>


          <button
            className="primary-button full-button"
            type="submit"
          >
            Login
          </button>

        </form>


        <p
          className="muted"
          style={{
            marginTop: 25,
            textAlign: "center"
          }}
        >
          Don't have an account?{" "}

          <Link
            to="/register"
            style={{
              color: "#202124",
              fontWeight: 700
            }}
          >
            Create one
          </Link>

        </p>

      </div>

    </div>
  );
}

export default Login;