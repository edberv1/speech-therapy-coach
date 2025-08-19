import React, { useEffect, useState } from "react";

function Dashboard({ refreshFlag }) {
  const [exercises, setExercises] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/exercises")
      .then((res) => res.json())
      .then((data) => setExercises(data.exercises))
      .catch((err) => console.log(err));
  }, [refreshFlag]); // refresh when exercises added

  return (
    <div>
      <h2>All Exercises</h2>
      <ul>
        {exercises.map((ex, index) => (
          <li key={index}>
            {ex.title} - {ex.description}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;
