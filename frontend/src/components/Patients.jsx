import React, { useEffect, useState } from "react";
import api from "../api/api.js";

const Patients = () => {
  const [patients, setPatients] = useState([]);
  const [form, setForm] = useState({ name: "", date_of_birth: "", phone: "", address: "", medical_notes: "" });

  const fetchPatients = async () => {
    const res = await api.get("/patients/");
    setPatients(res.data);
  };

  useEffect(() => { fetchPatients(); }, []);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post("/patients/", form);
      setForm({ name: "", date_of_birth: "", phone: "", address: "", medical_notes: "" });
      fetchPatients();
    } catch (err) {
      alert(err.response?.data?.error || "Failed to add patient");
    }
  };

  return (
    <div>
      <h2>Patients</h2>
      <form onSubmit={handleSubmit}>
        <input name="name" placeholder="Name" onChange={handleChange} required />
        <input type="date" name="date_of_birth" value={form.date_of_birth} onChange={handleChange} required/>
        <input name="phone" placeholder="Phone" onChange={handleChange} />
        <input name="address" placeholder="Address" onChange={handleChange} />
        <input name="medical_notes" placeholder="Medical Notes" onChange={handleChange} />
        <button type="submit">Add Patient</button>
      </form>

      <h3>My Patients</h3>
      <ul>
        {patients.map(p => (
          <li key={p.id}>{p.name} - {p.date_of_birth} - {p.phone}</li>
        ))}
      </ul>
    </div>
  );
};

export default Patients;
