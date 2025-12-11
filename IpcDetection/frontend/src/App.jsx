import React, { useState } from "react";
import "./index.css";

function App() {
  const [complaint, setComplaint] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleTextSubmit = async (e) => {
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

      if (!response.ok) throw new Error("Failed to fetch prediction.");

      const data = await response.json();
      setResult({ text: complaint, prediction: data });
    } catch (err) {
      setError("An error occurred while processing your request.");
    }
  };

  const handleFileSubmit = async (e) => {
    e.preventDefault();
    setResult(null);
    setError("");

    if (!file) {
      setError("Please select an image.");
      return;
    }

    const formData = new FormData();
    formData.append("image", file);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Failed to fetch prediction.");

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("An error occurred while processing the image.");
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Crime Prediction App</h1>

        {/* Text Input Form */}
        <div className="card">
          <h2>Predict from Text</h2>
          <form onSubmit={handleTextSubmit}>
            <textarea
              value={complaint}
              onChange={(e) => setComplaint(e.target.value)}
              placeholder="Enter your complaint here..."
            ></textarea>
            <button type="submit">Predict</button>
          </form>
        </div>

        {/* Image Upload Form */}
        <div className="card">
          <h2>Predict from Image</h2>
          <form onSubmit={handleFileSubmit}>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setFile(e.target.files[0])}
            />
            <button type="submit">Predict</button>
          </form>
        </div>

        {/* Error */}
        {error && <div className="error">{error}</div>}

        {/* Result */}
        {result && (
          <div className="result-card">
            <h2>Prediction Results</h2>
            {result.text && (
              <p>
                <strong>Extracted Text:</strong> {result.text}
              </p>
            )}
            <p>
              <strong>Crime:</strong> {result.prediction.crime}
            </p>
            <p>
              <strong>IPC Code:</strong> {result.prediction.ipc_code}
            </p>
            <p>
              <strong>Description:</strong> {result.prediction.description}
            </p>
            <p>
              <strong>Punishment:</strong> {result.prediction.punishment}
            </p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
