import React, { useEffect, useState } from "react";
import api from "../api/api.js";

import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";



const CalendarView = () => {
  const [patients, setPatients] = useState([]);
  const [therapists, setTherapists] = useState([]);
  const [events, setEvents] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    patient_id: "",
    therapist_id: "",
    date_time: "",
    duration_minutes: 60,
    notes: ""
  });

  const fetchPatients = async () => {
    const res = await api.get("/patients/");
    setPatients(res.data);
  };

  const fetchTherapists = async () => {
    const res = await api.get("/therapists/"); // <- consistent with backend
    setTherapists(res.data);
  };

  const fetchTherapies = async () => {
    const res = await api.get("/therapies/");
    const evs = res.data.map((t) => {
      const start = new Date(t.date_time);
      const end = new Date(start.getTime() + (t.duration_minutes || 60) * 60000);
      return {
        id: t.id,
        title: `${t.patient || "Patient"} → ${t.therapist || "Therapist"}`,
        start: start.toISOString(),
        end: end.toISOString()
      };
    });
    setEvents(evs);
  };

  useEffect(() => {
    fetchPatients();
    fetchTherapists();
    fetchTherapies();
  }, []);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    await api.post("/therapies/", form);
    setShowForm(false);
    setForm({ patient_id: "", therapist_id: "", date_time: "", duration_minutes: 60, notes: "" });
    fetchTherapies(); // refresh calendar
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h2>Therapies Calendar</h2>
        <button onClick={() => setShowForm(true)}>Add New Therapy</button>
      </div>

      {showForm && (
        <div style={modalStyles.backdrop}>
          <div style={modalStyles.modal}>
            <h3>New Therapy</h3>
            <form onSubmit={handleSubmit} style={{ display: "grid", gap: 8 }}>
              <select name="patient_id" value={form.patient_id} onChange={handleChange} required>
                <option value="">Select Patient</option>
                {patients.map((p) => (
                  <option key={p.id} value={p.id}>{p.name}</option>
                ))}
              </select>

              <select name="therapist_id" value={form.therapist_id} onChange={handleChange} required>
                <option value="">Select Therapist</option>
                {therapists.map((t) => (
                  <option key={t.id} value={t.id}>{t.name}</option>
                ))}
              </select>

              <input
                type="datetime-local"
                name="date_time"
                value={form.date_time}
                onChange={handleChange}
                required
              />

              <input
                type="number"
                min="15"
                step="15"
                name="duration_minutes"
                value={form.duration_minutes}
                onChange={handleChange}
                placeholder="Duration (minutes)"
              />

              <input
                name="notes"
                value={form.notes}
                onChange={handleChange}
                placeholder="Notes (optional)"
              />

              <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
                <button type="button" onClick={() => setShowForm(false)}>Cancel</button>
                <button type="submit">Create</button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div style={{ marginTop: 16 }}>
        <FullCalendar
          plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
          initialView="timeGridWeek"
          headerToolbar={{
            left: "prev,next today",
            center: "title",
            right: "dayGridMonth,timeGridWeek,timeGridDay"
          }}
          events={events}
          height="80vh"
        />
      </div>
    </div>
  );
};

const modalStyles = {
  backdrop: {
    position: "fixed", inset: 0, background: "rgba(0,0,0,0.4)",
    display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000
  },
  modal: {
    background: "#fff", padding: 16, borderRadius: 8, width: 400, maxWidth: "95vw"
  }
};

export default CalendarView;
