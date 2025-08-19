import React, { useEffect, useState } from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import api from "../api/api.js";

const CalendarView = () => {
  const [events, setEvents] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [therapists, setTherapists] = useState([]);
  const [patients, setPatients] = useState([]);
  const [form, setForm] = useState({
    therapist_id: "",
    patient_id: "",
    date_time: "",
    notes: "",
  });

  // Fetch all therapies
  const fetchTherapies = async () => {
    const res = await api.get("/therapies/");
    const evs = res.data.map((t) => ({
      id: t.id,
      title: `${t.patient} → ${t.therapist}`,
      start: t.date_time,
    }));
    setEvents(evs);
  };

  // Fetch all therapists
  const fetchTherapists = async () => {
    const res = await api.get("/therapists/"); // create this endpoint if not exists
    setTherapists(res.data);
  };

  // Fetch all patients
  const fetchPatients = async () => {
    const res = await api.get("/patients/");
    setPatients(res.data);
  };

  useEffect(() => {
    fetchTherapies();
    fetchTherapists();
    fetchPatients();
  }, []);

  // Handle form input change
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Submit new therapy
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post("/therapies/", form);
      setForm({ therapist_id: "", patient_id: "", date_time: "", notes: "" });
      setShowForm(false);
      fetchTherapies(); // refresh calendar immediately
    } catch (err) {
      alert(err.response?.data?.error || "Failed to add therapy");
    }
  };

  return (
    <div>
      <h2>Therapies Calendar</h2>
      <button onClick={() => setShowForm(true)}>Add New Therapy</button>

      {/* Therapy Form Modal */}
      {showForm && (
        <div className="modal">
          <form onSubmit={handleSubmit}>
            <select
              name="therapist_id"
              value={form.therapist_id}
              onChange={handleChange}
              required
            >
              <option value="">Select Therapist</option>
              {therapists.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name}
                </option>
              ))}
            </select>

            <select
              name="patient_id"
              value={form.patient_id}
              onChange={handleChange}
              required
            >
              <option value="">Select Patient</option>
              {patients.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name}
                </option>
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
              type="text"
              name="notes"
              placeholder="Notes"
              value={form.notes}
              onChange={handleChange}
            />

            <button type="submit">Add Therapy</button>
            <button type="button" onClick={() => setShowForm(false)}>
              Cancel
            </button>
          </form>
        </div>
      )}

      {/* Full Calendar */}
      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        initialView="timeGridWeek"
        events={events}
        headerToolbar={{
          left: "prev,next today",
          center: "title",
          right: "dayGridMonth,timeGridWeek,timeGridDay",
        }}
      />
    </div>
  );
};

export default CalendarView;
