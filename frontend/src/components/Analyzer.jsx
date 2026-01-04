// frontend/src/components/Analyzer.jsx

import { useState } from "react";
import { analyzeMessage } from "../services/api";

export default function Analyzer() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!message.trim()) {
      setError("Please enter a message to analyze");
      return;
    }

    setError("");
    setLoading(true);
    setResult(null);

    try {
      const data = await analyzeMessage(message, "email");
      setResult(data);
    } catch (err) {
      setError("Backend not responding. Is the server running?");
    }

    setLoading(false);
  };

  return (
    <div style={{ maxWidth: "700px", margin: "40px auto", padding: "20px" }}>
      <h2>Phishing Message Analyzer</h2>

      <textarea
        rows="6"
        style={{ width: "100%", padding: "10px" }}
        placeholder="Paste suspicious message here..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />

      <br /><br />

      <button onClick={handleAnalyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {error && (
        <p style={{ color: "red", marginTop: "15px" }}>{error}</p>
      )}

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h3>Verdict: {result.verdict}</h3>
          <p><strong>Risk Score:</strong> {result.risk_score}</p>

          {result.engine_results && (
            <>
              <h4>Engine Results</h4>
              <ul>
                {result.engine_results.map((engine, index) => (
                  <li key={index}>
                    {engine.engine_name} → {engine.verdict} ({engine.risk_score})
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}
