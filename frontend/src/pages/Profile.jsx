import React, { useEffect, useState, useContext } from "react";
import { StoreContext } from "../context/StoreContext";
import { Navigate } from "react-router-dom";
import "../styles/Profile.css";

function Profile() {
  const { user, setUser } = useContext(StoreContext);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    age: "",
    bio: "",
    phone_number: "",
  });

  const token = localStorage.getItem("token");

  // Restore user from localStorage if not in context
  useEffect(() => {
    if (!user) {
      const username = localStorage.getItem("username");
      if (username) setUser({ username });
    }
  }, [user, setUser]);

  if (!user || !token) return <Navigate to="/login" />;

  // Fetch profile on mount
  useEffect(() => {
    const fetchProfile = async () => {
      setLoading(true);
      setError("");

      try {
        const res = await fetch("http://localhost:5000/api/profile", {
          headers: { Authorization: `Bearer ${token}` },
        });

        const data = await res.json();

        if (res.ok) {
          if (!data.message) {
            setProfile(data);
            setFormData({
              first_name: data.first_name || "",
              last_name: data.last_name || "",
              age: data.age || "",
              bio: data.bio || "",
              phone_number: data.phone_number || "",
            });
          }
        } else {
          setError(data.error || data.message || "Failed to fetch profile");
        }
      } catch (err) {
        setError("Server not reachable");
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [token]);

  // Handle form input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  // Handle form submit (create/update profile)
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const method = profile ? "PUT" : "POST";

    try {
      const res = await fetch("http://localhost:5000/api/profile", {
        method: method,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (res.ok) {
        setProfile(data.profile || data);
        alert(`Profile ${method === "POST" ? "created" : "updated"} successfully`);
      } else {
        setError(data.error || data.message || "Something went wrong");
      }
    } catch (err) {
      setError("Server not reachable");
    }
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div className="profile-container">
      <h2 className="profile-title">Profile</h2>
      <p className="profile-welcome">Welcome, {user.username}!</p>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSubmit} className="profile-form">
        <input
          type="text"
          name="first_name"
          placeholder="First Name"
          value={formData.first_name}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="last_name"
          placeholder="Last Name"
          value={formData.last_name}
          onChange={handleChange}
        />
        <input
          type="number"
          name="age"
          placeholder="Age"
          value={formData.age}
          onChange={handleChange}
        />
        <input
          type="text"
          name="phone_number"
          placeholder="Phone Number"
          value={formData.phone_number}
          onChange={handleChange}
        />
        <textarea
          name="bio"
          placeholder="Bio"
          value={formData.bio}
          onChange={handleChange}
        />
        <button type="submit">{profile ? "Update Profile" : "Create Profile"}</button>
      </form>
    </div>
  );
}

export default Profile;
