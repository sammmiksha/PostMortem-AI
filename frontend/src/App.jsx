import { useState } from "react";
import api from "./services/api";

function App() {
  const [activeTab, setActiveTab] = useState("rootcause");

  // Part 1 State (Postmortem Generator)
  const [title, setTitle] = useState("");
  const [details, setDetails] = useState("");
  const [report, setReport] = useState(null);
  const [reportLoading, setReportLoading] = useState(false);

  // Part 2 State (Git Root Cause Analyzer)
  const [repoPath, setRepoPath] = useState("C:\\projects\\PostMortem-AI");
  const [stackTrace, setStackTrace] = useState(`Traceback (most recent call last):
  File "backend/app/main.py", line 21, in analyze_incident
    report = generator.generate(request.incident_details)
RuntimeError: ConnectionTimeoutError: Failed to connect to PostgreSQL database pool at port 2907`);
  const [incidentSummary, setIncidentSummary] = useState("Checkout API timed out due to database connection exhaustion");
  const [rootCauseResult, setRootCauseResult] = useState(null);
  const [rootCauseLoading, setRootCauseLoading] = useState(false);

  // Part 3 RAG Search state
  const [searchQuery, setSearchQuery] = useState("");

  // Handler for Part 1: Incident Analysis
  const analyzeIncident = async () => {
    try {
      setReportLoading(true);
      if (title.length < 5) {
        alert("Title must be at least 5 characters");
        return;
      }
      if (details.length < 20) {
        alert("Incident details must be at least 20 characters");
        return;
      }
      const response = await api.post("/incidents/analyze", {
        title,
        incident_details: details,
      });
      setReport(response.data);
    } catch (error) {
      console.error(error);
      alert("Failed to analyze incident. Please check backend API.");
    } finally {
      setReportLoading(false);
    }
  };

  // Handler for Part 2: Git Root Cause Analysis
  const runRootCauseAnalysis = async () => {
    try {
      setRootCauseLoading(true);
      if (stackTrace.trim().length < 10) {
        alert("Please provide a valid stack trace or traceback log.");
        return;
      }
      const response = await api.post("/api/root-cause/analyze", {
        repo_path: repoPath,
        stack_trace: stackTrace,
        incident_summary: incidentSummary,
      });
      setRootCauseResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Root cause analysis failed. Please verify git repository path and backend status.");
    } finally {
      setRootCauseLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Top Navbar */}
      <header className="navbar">
        <div className="brand">
          <div className="brand-icon">P</div>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
              <span className="brand-title">PostMortem-AI</span>
              <span className="brand-badge">Part 2 Active</span>
            </div>
            <div style={{ fontSize: "0.75rem", color: "var(--text-dim)" }}>
              AI Incident Intelligence & Git Root Cause Platform
            </div>
          </div>
        </div>

        <nav className="nav-tabs">
          <button
            className={`nav-tab ${activeTab === "postmortem" ? "active" : ""}`}
            onClick={() => setActiveTab("postmortem")}
          >
            <span>⚡ Postmortem Generator</span>
          </button>

          <button
            className={`nav-tab ${activeTab === "rootcause" ? "active" : ""}`}
            onClick={() => setActiveTab("rootcause")}
          >
            <span>🔍 Git Root Cause</span>
            <span className="tab-badge">Part 2</span>
          </button>

          <button
            className={`nav-tab ${activeTab === "memory" ? "active" : ""}`}
            onClick={() => setActiveTab("memory")}
          >
            <span>🧠 Memory & RAG</span>
            <span className="tab-badge">Part 3</span>
          </button>

          <button
            className={`nav-tab ${activeTab === "prevention" ? "active" : ""}`}
            onClick={() => setActiveTab("prevention")}
          >
            <span>🛡️ Prevention Engine</span>
            <span className="tab-badge">Part 4</span>
          </button>

          <button
            className={`nav-tab ${activeTab === "analytics" ? "active" : ""}`}
            onClick={() => setActiveTab("analytics")}
          >
            <span>📊 Analytics</span>
            <span className="tab-badge">Part 5</span>
          </button>
        </nav>

        <div className="status-pill">
          <div className="status-dot"></div>
          <span>Engine Online</span>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="main-content">
        {/* TAB 1: Incident Postmortem Generator */}
        {activeTab === "postmortem" && (
          <div>
            <div className="page-header">
              <h1 className="page-title">AI Incident Report Generator</h1>
              <p className="page-subtitle">
                Paste incident logs or details below to generate a structured SRE postmortem report.
              </p>
            </div>

            <div className="panel">
              <div className="form-group">
                <label className="form-label">Incident Title</label>
                <input
                  className="form-input"
                  placeholder="e.g. Production Database Connection Exhaustion during Peak Traffic"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Incident Log / Description</label>
                <textarea
                  className="form-textarea"
                  rows="8"
                  placeholder="Paste incident timeline, error logs, metrics, or description (minimum 20 characters)..."
                  value={details}
                  onChange={(e) => setDetails(e.target.value)}
                />
              </div>

              <button
                className="btn-primary"
                onClick={analyzeIncident}
                disabled={reportLoading}
              >
                {reportLoading ? "Analyzing Incident with AI..." : "⚡ Generate AI Postmortem"}
              </button>
            </div>

            {report && report.report && (
              <div className="panel" style={{ borderLeft: "4px solid #6366f1" }}>
                <div className="panel-header">
                  <h2 className="panel-title">📄 AI Generated Postmortem Report</h2>
                  <span style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>
                    Report ID: #{report.id}
                  </span>
                </div>

                <div className="grid-2" style={{ marginBottom: "1.5rem" }}>
                  <div className="ai-box">
                    <div className="ai-box-title">Executive Summary</div>
                    <p style={{ color: "var(--text-main)" }}>{report.report.summary}</p>
                  </div>

                  <div className="ai-box" style={{ borderLeftColor: "#f43f5e" }}>
                    <div className="ai-box-title" style={{ color: "#f43f5e" }}>Root Cause</div>
                    <p style={{ color: "var(--text-main)" }}>{report.report.root_cause}</p>
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">System & Business Impact</label>
                  <p style={{ background: "var(--bg-input)", padding: "1rem", borderRadius: "var(--radius-sm)" }}>
                    {report.report.impact}
                  </p>
                </div>

                <div className="form-group">
                  <label className="form-label">Actionable Recommendations</label>
                  <ul style={{ paddingLeft: "1.5rem", color: "var(--text-main)" }}>
                    {report.report.recommendations?.map((rec, index) => (
                      <li key={index} style={{ marginBottom: "0.5rem" }}>{rec}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>
        )}

        {/* TAB 2: Git Root Cause Analyzer (Part 2 Core) */}
        {activeTab === "rootcause" && (
          <div>
            <div className="page-header">
              <h1 className="page-title">Git Root Cause Analyzer</h1>
              <p className="page-subtitle">
                Correlate production stack traces against commit history to isolate the introducing commit.
              </p>
            </div>

            <div className="panel">
              <div className="grid-2">
                <div className="form-group">
                  <label className="form-label">Target Git Repository Path</label>
                  <input
                    className="form-input"
                    value={repoPath}
                    onChange={(e) => setRepoPath(e.target.value)}
                    placeholder="Path to repository (e.g. C:\projects\PostMortem-AI)"
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Incident Context / Summary</label>
                  <input
                    className="form-input"
                    value={incidentSummary}
                    onChange={(e) => setIncidentSummary(e.target.value)}
                    placeholder="Brief summary of what went wrong"
                  />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Stack Trace / Exception Log</label>
                <textarea
                  className="form-textarea"
                  rows="7"
                  value={stackTrace}
                  onChange={(e) => setStackTrace(e.target.value)}
                  placeholder="Paste Python, Node, Java, or Go stack trace here..."
                />
              </div>

              <button
                className="btn-primary"
                onClick={runRootCauseAnalysis}
                disabled={rootCauseLoading}
              >
                {rootCauseLoading ? "Scanning Repository & Analyzing Commits..." : "🔍 Investigate Root Cause Commits"}
              </button>
            </div>

            {/* Analysis Results Display */}
            {rootCauseResult && (
              <div>
                {/* Parsed Stacktrace Clues Header */}
                <div className="panel" style={{ background: "rgba(30, 41, 59, 0.5)" }}>
                  <div className="panel-header">
                    <h3 className="panel-title">🧩 Parsed Stack Trace Clues</h3>
                  </div>
                  <div style={{ display: "flex", gap: "1.5rem", flexWrap: "wrap", fontSize: "0.9rem" }}>
                    <div>
                      <span style={{ color: "var(--text-muted)" }}>Target File: </span>
                      <strong style={{ color: "#818cf8" }}>{rootCauseResult.stacktrace?.file || "None parsed"}</strong>
                    </div>
                    <div>
                      <span style={{ color: "var(--text-muted)" }}>Line Number: </span>
                      <strong style={{ color: "#818cf8" }}>{rootCauseResult.stacktrace?.line || "N/A"}</strong>
                    </div>
                    <div>
                      <span style={{ color: "var(--text-muted)" }}>Function: </span>
                      <strong style={{ color: "#818cf8" }}>{rootCauseResult.stacktrace?.function || "N/A"}</strong>
                    </div>
                    <div>
                      <span style={{ color: "var(--text-muted)" }}>Error Type: </span>
                      <strong style={{ color: "#f43f5e" }}>{rootCauseResult.stacktrace?.error || "Unknown Error"}</strong>
                    </div>
                  </div>
                </div>

                {/* Candidate Commits List */}
                <h3 style={{ fontSize: "1.2rem", fontWeight: "700", marginBottom: "1rem" }}>
                  Top Suspicious Commit Candidates ({rootCauseResult.candidate_commits?.length || 0})
                </h3>

                {rootCauseResult.candidate_commits?.map((commit, idx) => {
                  const confidence = commit.ai_confidence || commit.score || 50;
                  const confidenceClass = confidence >= 70 ? "high" : confidence >= 40 ? "med" : "low";

                  return (
                    <div key={idx} className="commit-card">
                      <div className="commit-header">
                        <div>
                          <span className="commit-hash">{commit.hash?.substring(0, 8)}</span>
                          <span style={{ marginLeft: "0.75rem" }} className="commit-author">
                            by <strong>{commit.author}</strong> on {commit.date ? new Date(commit.date).toLocaleDateString() : "Recent"}
                          </span>
                        </div>
                        <div className={`badge-confidence ${confidenceClass}`}>
                          <span>{confidence}% Risk Score</span>
                        </div>
                      </div>

                      <div className="commit-msg">{commit.message}</div>

                      {/* AI Reasoning Box */}
                      {commit.ai_reason && (
                        <div className="ai-box">
                          <div className="ai-box-title">🤖 AI Root Cause Review</div>
                          <div>{commit.ai_reason}</div>
                        </div>
                      )}

                      {/* Heuristic Breakdown */}
                      <div style={{ marginBottom: "0.75rem", fontSize: "0.85rem" }}>
                        <span style={{ color: "var(--text-muted)" }}>Ranking Factors: </span>
                        {commit.reasons?.map((r, i) => (
                          <span key={i} className="diff-tag">{r}</span>
                        ))}
                      </div>

                      {/* Code Diff Changes */}
                      {commit.changes_diff?.length > 0 && (
                        <div>
                          <div style={{ fontSize: "0.8rem", fontWeight: "600", color: "var(--text-muted)", marginBottom: "0.4rem" }}>
                            Modified Files & Patch Snippet:
                          </div>
                          {commit.changes_diff.map((diff, dIdx) => (
                            <div key={dIdx} style={{ marginBottom: "0.5rem" }}>
                              <div style={{ marginBottom: "0.25rem" }}>
                                <span className="diff-tag" style={{ background: "rgba(99, 102, 241, 0.2)", color: "#a5b4fc" }}>
                                  {diff.category}
                                </span>
                                <span className="diff-tag">{diff.change_type}</span>
                                <strong style={{ fontSize: "0.85rem", color: "#f3f4f6" }}>{diff.file}</strong>
                              </div>
                              {diff.summary && (
                                <pre className="diff-container">{diff.summary}</pre>
                              )}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* TAB 3: Incident Memory System (Part 3 Preview & Architecture) */}
        {activeTab === "memory" && (
          <div>
            <div className="page-header">
              <h1 className="page-title">Incident Memory System (RAG)</h1>
              <p className="page-subtitle">
                Semantic vector search and pattern detection engine (Part 3 Roadmap).
              </p>
            </div>

            <div className="panel">
              <div className="form-group">
                <label className="form-label">Semantic Memory Search</label>
                <div style={{ display: "flex", gap: "0.75rem" }}>
                  <input
                    className="form-input"
                    placeholder="e.g. Show all database connection pool exhaustion incidents..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                  />
                  <button className="btn-primary" style={{ whiteSpace: "nowrap" }}>
                    🔍 Search Vector Memory
                  </button>
                </div>
              </div>
            </div>

            <div className="grid-2">
              <div className="panel">
                <h3 className="panel-title">📌 Historical Incident Vector Store</h3>
                <p style={{ fontSize: "0.9rem", color: "var(--text-muted)", marginTop: "0.5rem" }}>
                  Powered by <code>pgvector</code> and <code>all-MiniLM-L6-v2</code> (384d embeddings). Stores key root causes, resolutions, and affected services.
                </p>
              </div>

              <div className="panel">
                <h3 className="panel-title">🔁 Automated Pattern Detection</h3>
                <p style={{ fontSize: "0.9rem", color: "var(--text-muted)", marginTop: "0.5rem" }}>
                  Discovers recurring failure modes across 90-day windows (Database, Auth, Networking, Config) to prevent repeat fires.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* TAB 4: Prevention Engine (Part 4 Preview) */}
        {activeTab === "prevention" && (
          <div>
            <div className="page-header">
              <h1 className="page-title">Prevention Intelligence Engine</h1>
              <p className="page-subtitle">
                Auto-generate regression tests, Prometheus alerts, and runbooks (Part 4 Roadmap).
              </p>
            </div>

            <div className="grid-2">
              <div className="panel">
                <h3 className="panel-title">🧪 Auto-Generated Pytest Regression Tests</h3>
                <pre className="diff-container" style={{ maxHeight: "none", marginTop: "0.75rem" }}>
{`def test_prevent_db_pool_exhaustion():
    # Auto-generated regression test
    pool = create_connection_pool(max_connections=10)
    with pytest.raises(TimeoutError):
        for _ in range(11):
            pool.acquire_connection(timeout=0.1)`}
                </pre>
              </div>

              <div className="panel">
                <h3 className="panel-title">🔔 Monitoring & Runbook Artifacts</h3>
                <pre className="diff-container" style={{ maxHeight: "none", marginTop: "0.75rem" }}>
{`# Prometheus Alert Rule
alert: PostgresPoolUsageHigh
expr: pg_stat_activity_count / pg_max_connections > 0.85
for: 2m
labels:
  severity: critical
annotations:
  summary: DB Connection Pool > 85%`}
                </pre>
              </div>
            </div>
          </div>
        )}

        {/* TAB 5: Analytics Dashboard (Part 5 Preview) */}
        {activeTab === "analytics" && (
          <div>
            <div className="page-header">
              <h1 className="page-title">Reliability Analytics Dashboard</h1>
              <p className="page-subtitle">
                Executive operational health metrics and MTTR trends (Part 5 Roadmap).
              </p>
            </div>

            <div className="grid-2" style={{ marginBottom: "1.5rem" }}>
              <div className="panel" style={{ textAlign: "center" }}>
                <div style={{ fontSize: "2rem", fontWeight: "800", color: "#818cf8" }}>18.4 mins</div>
                <div style={{ color: "var(--text-muted)", fontSize: "0.85rem", textTransform: "uppercase" }}>
                  Mean Time To Resolution (MTTR)
                </div>
              </div>

              <div className="panel" style={{ textAlign: "center" }}>
                <div style={{ fontSize: "2rem", fontWeight: "800", color: "#10b981" }}>99.94%</div>
                <div style={{ color: "var(--text-muted)", fontSize: "0.85rem", textTransform: "uppercase" }}>
                  System Availability
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;