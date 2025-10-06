import React, { useContext, useState } from "react";
import { StoreContext } from "../context/StoreContext";
import { useNavigate } from "react-router-dom";
import "../styles/Login.css";

function Login() {
  const { login } = useContext(StoreContext);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = () => {
    if (login(username, password)) {
      navigate("/profile");
    } else {
      alert("Invalid credentials (use user/pass)");
    }
  };

  return (
    <div className="login-container">
      <h2 className="login-title">Login</h2>
      <input
        type="text"
        placeholder="Username"
        className="login-input"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        className="login-input"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleLogin} className="login-btn">
        Login
      </button>
    </div>
  );
}

export default Login;
