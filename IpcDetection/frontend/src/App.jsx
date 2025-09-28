import React, { useState } from "react";
import "./index.css"
function App() {
  const [complaint, setComplaint] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult(null);
    setError("");

    if (!complaint.trim()) {
      setError("Please enter a complaint.");
      return;
    }

    

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ complaint }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch prediction.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("An error occurred while processing your request.");
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Crime Prediction App</h1>
        <form onSubmit={handleSubmit}>
          <textarea
            value={complaint}
            onChange={(e) => setComplaint(e.target.value)}
            placeholder="Enter your complaint here..."
          ></textarea>
          <button type="submit">Submit</button>
        </form>
        {error && <div className="error">{error}</div>}
        {result && (
          <div className="result">
            <h3>Prediction Results</h3>
            <p><strong>Crime:</strong> {result.crime}</p>
            <p><strong>IPC Code:</strong> {result.ipc_code}</p>
            <p><strong>Description:</strong> {result.description}</p>
            <p><strong>Punishment:</strong> {result.punishment}</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
