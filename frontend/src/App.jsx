import { useState } from "react";
import api from "./services/api";

function App() {
  const [title, setTitle] = useState("");
  const [details, setDetails] = useState("");
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeIncident = async () => {
    try {
      setLoading(true);
      if (title.length < 5) {
        alert("Title must be at least 5 characters");
        return;
      }

      if (details.length < 20) {
        alert("Incident details must be at least 20 characters");
        return;
      }
      const response = await api.post(
        "/incidents/analyze",
        {
          title,
          incident_details: details,
        }
      );

      setReport(response.data);
    } catch (error) {
      console.error(error);
      alert("Failed to analyze incident");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Incident Intelligence Engine</h1>

      <input
        placeholder="Incident Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        style={{
          width: "100%",
          marginBottom: "1rem",
          padding: "10px",
        }}
      />

      <textarea
        rows="8"
        placeholder="Describe the incident..."
        value={details}
        onChange={(e) => setDetails(e.target.value)}
        style={{
          width: "100%",
          marginBottom: "1rem",
          padding: "10px",
        }}
      />

      <button onClick={analyzeIncident} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {report && (
        <div
          style={{
            marginTop: "2rem",
            border: "1px solid #ccc",
            padding: "1rem",
          }}
        >
          <h2>Generated Report</h2>

          <h2>Summary</h2>
          <p>{report.report.summary}</p>

          <h2>Root Cause</h2>
          <p>{report.report.root_cause}</p>

          <h2>Impact</h2>
          <p>{report.report.impact}</p>

          <h2>Recommendations</h2>

          <ul>
            {report.report.recommendations.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;