import { Link } from "react-router-dom";
import "../App.css";

function Landing() {
  return (
    <div className="landing">

      <nav className="landing-nav">
        <div className="logo">
          MuveFit
        </div>

        <Link to="/login">
          Login
        </Link>
      </nav>


      <main className="hero">

        <section>

          <p
            style={{
              marginTop: 0,
              color: "#202124",
              fontWeight: 700
            }}
          >
            MOVE BETTER.
          </p>

          <h1>
            Train smarter.
            <br />
            Move safer.
          </h1>

          <p>
            AI-powered exercise analysis that helps
            you understand your movement, improve your
            form and track your progress.
          </p>

          <div className="hero-actions">

            <Link
              to="/register"
              className="primary-button"
            >
              Create Account
            </Link>

            <Link
              to="/login"
              className="secondary-button"
            >
              Login
            </Link>

          </div>

        </section>


        <section className="hero-art">

          <div className="hero-circle"></div>

          <div className="hero-word">
            MUVE
          </div>

        </section>

      </main>

    </div>
  );
}

export default Landing;