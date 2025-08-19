import React, { useState } from "react";
import api from "../api/api.js";
import { useNavigate } from "react-router-dom";

const Signup = () => {
  const [form, setForm] = useState({ name: "", email: "", password: "", phone: "" });
  const navigate = useNavigate();

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post("/auth/register", form);
      alert("Registered successfully! Please login.");
      navigate("/login");
    } catch (err) {
      alert(err.response?.data?.error || "Registration failed");
    }
  };

  return (
    <div>
      <h2>Therapist Signup</h2>
      <form onSubmit={handleSubmit}>
        <input name="name" placeholder="Name" onChange={handleChange} required />
        <input name="email" placeholder="Email" type="email" onChange={handleChange} required />
        <input name="password" placeholder="Password" type="password" onChange={handleChange} required />
        <input name="phone" placeholder="Phone" onChange={handleChange} />
        <button type="submit">Signup</button>
      </form>
    </div>
  );
};

export default Signup;
