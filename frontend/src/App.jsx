import React, { useState } from "react";
import Dashboard from "./components/Dashboard";
import AddExercise from "./components/AddExercise";

function App() {
  const [refreshFlag, setRefreshFlag] = useState(false);

  const refresh = () => setRefreshFlag(!refreshFlag);

  return (
    <div>
      <h1>Speech Therapy Coach</h1>
      <AddExercise refresh={refresh} />
      <Dashboard refreshFlag={refreshFlag} />
    </div>
  );
}

export default App;
