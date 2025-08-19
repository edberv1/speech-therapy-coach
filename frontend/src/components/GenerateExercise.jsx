import React, { useState } from "react";

function GenerateExercise({ refresh }) {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!prompt) return;
    setLoading(true);

    try {
      // Call AI generate endpoint
      const res = await fetch("http://127.0.0.1:5000/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
      });

      const data = await res.json();
      if (data.error) {
        alert("Error: " + data.error);
      } else {
        const exerciseText = data.exercise;

        // Automatically save to database
        await fetch("http://127.0.0.1:5000/api/exercises", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ title: prompt, description: exerciseText })
        });

        refresh(); // refresh dashboard
        setPrompt(""); // clear input
      }
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h3>Generate Exercise</h3>
      <input
        type="text"
        placeholder="Enter prompt, e.g., Practice R sounds"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button onClick={handleGenerate} disabled={loading}>
        {loading ? "Generating..." : "Generate & Save"}
      </button>
    </div>
  );
}

export default GenerateExercise;
