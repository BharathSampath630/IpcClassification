import React, { useState } from "react";
import "./index.css";

function App() {
  const [complaint, setComplaint] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleTextSubmit = async (e) => {
    e.preventDefault();
    setResult(null);
    setError("");

    if (!complaint.trim()) {
      setError("Please enter a complaint description.");
      return;
    }

    setLoading(true);
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
      setError("Server error. Ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleFileSubmit = async (e) => {
    e.preventDefault();
    setResult(null);
    setError("");

    if (!file) {
      setError("Please select an image first.");
      return;
    }

    const formData = new FormData();
    formData.append("image", file);

    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Failed to fetch prediction.");

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("Error processing image. Try a different file.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        
        <header>
          <h1>AI Legal Assistant</h1>
          <p className="subtitle">Automated IPC Code & Crime Analysis</p>
        </header>

        {/* Error Notification */}
        {error && <div className="error-msg">⚠️ {error}</div>}

        {/* Input Grid */}
        <div className="forms-grid">
          
          {/* Card 1: Text Analysis */}
          <div className="card">
            <h2>📝 Text Analysis</h2>
            <form onSubmit={handleTextSubmit} style={{display: 'flex', flexDirection: 'column', height: '100%'}}>
              <textarea
                value={complaint}
                onChange={(e) => setComplaint(e.target.value)}
                placeholder="Describe the incident in detail..."
              ></textarea>
              <button type="submit" disabled={loading}>
                {loading ? "Analyzing..." : "Analyze Complaint"}
              </button>
            </form>
          </div>

          {/* Card 2: Image Analysis */}
          <div className="card">
            <h2>📸 Evidence Analysis</h2>
            <form onSubmit={handleFileSubmit} style={{display: 'flex', flexDirection: 'column', height: '100%'}}>
              <div style={{flexGrow: 1, display:'flex', alignItems:'center'}}>
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => setFile(e.target.files[0])}
                />
              </div>
              <button type="submit" disabled={loading}>
                {loading ? "Scanning..." : "Scan Image"}
              </button>
            </form>
          </div>

        </div>

        {/* Result Section */}
        {result && (
          <div className="result-section">
            <div className="result-header">
              <h2>Analysis Report</h2>
              <div className="result-badge">CONFIRMED</div>
            </div>
            
            <div className="result-grid">
              {result.text && (
                <div className="info-row">
                  <span className="info-label">Input Text</span>
                  <span className="info-value">"{result.text}"</span>
                </div>
              )}
              
              <div className="info-row">
                <span className="info-label">Identified Crime</span>
                <span className="info-value" style={{color: '#d63031', fontWeight: 'bold'}}>
                  {result.prediction.crime}
                </span>
              </div>

              <div className="info-row">
                <span className="info-label">IPC Section</span>
                <span className="info-value">{result.prediction.ipc_code}</span>
              </div>

              <div className="info-row">
                <span className="info-label">Legal Description</span>
                <span className="info-value">{result.prediction.description}</span>
              </div>

              <div className="info-row">
                <span className="info-label">Standard Punishment</span>
                <span className="info-value">{result.prediction.punishment}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;