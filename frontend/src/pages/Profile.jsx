import React, { useContext } from "react";
import { StoreContext } from "../context/StoreContext";
import { Navigate } from "react-router-dom";
import "../styles/Profile.css";

function Profile() {
  const { user } = useContext(StoreContext);

  if (!user) return <Navigate to="/login" />;

  return (
    <div className="profile-container">
      <h2 className="profile-title">Profile</h2>
      <p className="profile-welcome">Welcome, {user.username}!</p>
    </div>
  );
}

export default Profile;
