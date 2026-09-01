import { Link, useNavigate } from "react-router-dom";
import "../App.css";

function Register() {

  const navigate = useNavigate();

  function handleRegister(e) {
    e.preventDefault();

    // Temporary frontend registration.
    // Backend will handle real accounts later.

    navigate("/dashboard");
  }

  return (
    <div className="auth-page">

      <div className="auth-card">

        <div className="logo">
          MuveFit
        </div>

        <h1 style={{ marginTop: 30 }}>
          Create your account.
        </h1>

        <p className="muted">
          Start understanding your movement.
        </p>


        <form onSubmit={handleRegister}>

          <div className="form-group">
            <label>Name</label>

            <input
              type="text"
              placeholder="Your name"
              required
            />
          </div>


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
              placeholder="Create a password"
              required
            />
          </div>


          <button
            className="primary-button full-button"
            type="submit"
          >
            Create Account
          </button>

        </form>


        <p
          className="muted"
          style={{
            marginTop: 25,
            textAlign: "center"
          }}
        >
          Already have an account?{" "}

          <Link
            to="/login"
            style={{
              color: "#202124",
              fontWeight: 700
            }}
          >
            Login
          </Link>

        </p>

      </div>

    </div>
  );
}

export default Register;