import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { StoreContext } from "../context/StoreContext";
import "../styles/Navbar.css";  // import css

function Navbar() {
  const { cart, user, logout } = useContext(StoreContext);

  return (
    <nav className="navbar">
      <h1>MyShop</h1>
      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/cart">Cart ({cart.length})</Link>
        <Link to="/orders">Orders</Link>
        {user ? (
          <>
            <Link to="/profile">Profile</Link>
            <button onClick={logout}>Logout</button>
          </>
        ) : (
          <Link to="/login">Login</Link>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
