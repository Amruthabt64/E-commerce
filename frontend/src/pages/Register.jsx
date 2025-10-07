import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Register.css";

function Register() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [message, setMessage] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const response = await fetch("http://localhost:5000/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("Registered successfully! Please login.");
        setTimeout(() => navigate("/login"), 1500);
      } else {
        // Display backend error if any, otherwise default message
        setMessage(
          data.error ||
            data.message ||
            "Email must be valid & password ≥8 chars with 1×A–Z, 1×a–z, 1×0–9, 1×@#$%."
        );
      }
    } catch (err) {
      setMessage("Server not reachable");
    }
  };

  return (
    <div className="register-container">
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        {/* Email input */}
        <input
          className="register-input"
          type="email"
          placeholder="Email"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <br />

        {/* Password input with toggle */}
        <div style={{ position: "relative" }}>
          <input
            className="register-input"
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <span
            onClick={() => setShowPassword((prev) => !prev)}
            style={{
              position: "absolute",
              right: "10px",
              top: "50%",
              transform: "translateY(-50%)",
              cursor: "pointer",
              userSelect: "none",
            }}
          >
            {showPassword ? "👁️" : "🙈"}
          </span>
        </div>
        <br />

        <button type="submit" className="register-button">
          Register
        </button>
      </form>

      {message && <p style={{ color: message.includes("success") ? "green" : "red" }}>{message}</p>}
    </div>
  );
}

export default Register;
