import { useState, useEffect } from "react";
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

  // Part 3 RAG Search & Pattern state
  const [searchQuery, setSearchQuery] = useState("Database connection pool timeout during peak traffic");
  const [searchResults, setSearchResults] = useState([]);
  const [memoryLoading, setMemoryLoading] = useState(false);
  const [patternsData, setPatternsData] = useState(null);

  // Part 4 Prevention Engine state
  const [prevSummary, setPrevSummary] = useState("PostgreSQL Database Connection Pool Exhaustion during Flash Sale");
  const [prevRootCause, setPrevRootCause] = useState("Unbounded db connection leak in payment checkout handler due to missing connection close in exception block");
  const [prevCategory, setPrevCategory] = useState("Database");
  const [preventionPkg, setPreventionPkg] = useState(null);
  const [preventionLoading, setPreventionLoading] = useState(false);
  const [artifactTab, setArtifactTab] = useState("test");

  // Part 5 Analytics & Integrations state
  const [analyticsData, setAnalyticsData] = useState(null);
  const [jiraNotice, setJiraNotice] = useState(null);
  const [slackNotice, setSlackNotice] = useState(null);
  const [currentUser, setCurrentUser] = useState({ name: "Samiksha Patil", email: "engineer@company.com", role: "Engineer" });

  useEffect(() => {
    if (activeTab === "memory") {
      fetchPatterns();
      runMemorySearch();
    } else if (activeTab === "analytics") {
      fetchAnalytics();
    }
  }, [activeTab]);

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

  // Handler for Part 3: Memory Vector RAG Search
  const runMemorySearch = async () => {
    try {
      setMemoryLoading(true);
      const response = await api.post("/api/memory/search", {
        query: searchQuery,
        top_k: 5
      });
      setSearchResults(response.data.results || []);
    } catch (error) {
      console.error("Memory search error:", error);
    } finally {
      setMemoryLoading(false);
    }
  };

  const fetchPatterns = async () => {
    try {
      const response = await api.get("/api/memory/patterns");
      setPatternsData(response.data);
    } catch (error) {
      console.error("Pattern fetch error:", error);
    }
  };

  // Handler for Part 4: Prevention Package Generation
  const generatePreventionPackage = async () => {
    try {
      setPreventionLoading(true);
      const response = await api.post("/api/prevention/generate", {
        summary: prevSummary,
        root_cause: prevRootCause,
        category: prevCategory
      });
      setPreventionPkg(response.data);
    } catch (error) {
      console.error("Prevention generation error:", error);
      alert("Failed to generate prevention package.");
    } finally {
      setPreventionLoading(false);
    }
  };

  const downloadPackage = () => {
    if (!preventionPkg) return;
    const blob = new Blob([JSON.stringify(preventionPkg, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `prevention_package_${prevCategory.toLowerCase()}.json`;
    a.click();
  };

  // Handlers for Part 5: Analytics & Integrations
  const fetchAnalytics = async () => {
    try {
      const response = await api.get("/api/analytics/metrics");
      setAnalyticsData(response.data);
    } catch (error) {
      console.error("Analytics fetch error:", error);
    }
  };

  const triggerJiraIntegration = async () => {
    try {
      const response = await api.post("/api/analytics/jira/create-issue", {
        summary: "Deploy PgBouncer Proxy Middleware for Connection Pooling",
        description: "Prevent database connection pool exhaustion during flash sale events.",
        priority: "High"
      });
      setJiraNotice(response.data);
    } catch (error) {
      console.error("Jira error:", error);
    }
  };

  const triggerSlackIntegration = async () => {
    try {
      const response = await api.post("/api/analytics/slack/send-alert", {
        title: "PostgreSQL Pool Exhaustion",
        summary: "Unbounded db connection leak in payment checkout handler.",
        root_cause: "Connection leak at payment.py line 245"
      });
      setSlackNotice(response.data);
    } catch (error) {
      console.error("Slack error:", error);
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
              <span className="brand-badge" style={{ background: "rgba(16, 185, 129, 0.2)", color: "#10b981", borderColor: "rgba(16, 185, 129, 0.4)" }}>
                Part 5 Production Platform
              </span>
            </div>
            <div style={{ fontSize: "0.75rem", color: "var(--text-dim)" }}>
              Enterprise Incident Intelligence Platform (Auth, RAG, Integrations & Analytics)
            </div>
          </div>
        </div>

        <nav className="nav-tabs">
          <button
            className={`nav-tab ${activeTab === "postmortem" ? "active" : ""}`}
            onClick={() => setActiveTab("postmortem")}
          >
            <span>Postmortem</span>
          </button>

          <button
            className={`nav-tab ${activeTab === "rootcause" ? "active" : ""}`}
            onClick={() => setActiveTab("rootcause")}
          >
            <span>Git Root Cause</span>
            <span className="tab-badge">Part 2</span>
          </button>

          <button
            className={`nav-tab ${activeTab === "memory" ? "active" : ""}`}
            onClick={() => setActiveTab("memory")}
          >
            <span>RAG Memory</span>
            <span className="tab-badge">Part 3</span>
          </button>

          <button
            className={`nav-tab ${activeTab === "prevention" ? "active" : ""}`}
            onClick={() => setActiveTab("prevention")}
          >
            <span>Prevention Engine</span>
            <span className="tab-badge">Part 4</span>
          </button>

          <button
            className={`nav-tab ${activeTab === "analytics" ? "active" : ""}`}
            onClick={() => setActiveTab("analytics")}
          >
            <span>Enterprise Analytics</span>
            <span className="tab-badge" style={{ background: "#10b981" }}>Part 5</span>
          </button>
        </nav>

        <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
          <div style={{ fontSize: "0.8rem", textAlign: "right" }}>
            <div style={{ color: "#fff", fontWeight: "600" }}>{currentUser.name}</div>
            <div style={{ color: "var(--text-muted)", fontSize: "0.7rem" }}>Role: {currentUser.role}</div>
          </div>
          <div className="status-pill">
            <div className="status-dot"></div>
            <span>Platform v5.0</span>
          </div>
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
                {reportLoading ? "Analyzing Incident with AI..." : "Generate AI Postmortem"}
              </button>
            </div>

            {report && report.report && (
              <div className="panel" style={{ borderLeft: "4px solid #6366f1" }}>
                <div className="panel-header">
                  <h2 className="panel-title">AI Generated Postmortem Report</h2>
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

        {/* TAB 2: Git Root Cause Analyzer */}
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
                {rootCauseLoading ? "Scanning Repository & Analyzing Commits..." : "Investigate Root Cause Commits"}
              </button>
            </div>

            {/* Analysis Results Display */}
            {rootCauseResult && (
              <div>
                <div className="panel" style={{ background: "rgba(30, 41, 59, 0.5)" }}>
                  <div className="panel-header">
                    <h3 className="panel-title">Parsed Stack Trace Clues</h3>
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

                      {commit.ai_reason && (
                        <div className="ai-box">
                          <div className="ai-box-title">AI Root Cause Review</div>
                          <div>{commit.ai_reason}</div>
                        </div>
                      )}

                      <div style={{ marginBottom: "0.75rem", fontSize: "0.85rem" }}>
                        <span style={{ color: "var(--text-muted)" }}>Ranking Factors: </span>
                        {commit.reasons?.map((r, i) => (
                          <span key={i} className="diff-tag">{r}</span>
                        ))}
                      </div>

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

        {/* TAB 3: Incident Memory System */}
        {activeTab === "memory" && (
          <div>
            <div className="page-header">
              <h1 className="page-title">Incident Memory System (RAG + Knowledge Base)</h1>
              <p className="page-subtitle">
                Retrieve historical incidents using natural language semantic vector search & detect recurring failure patterns across system memory.
              </p>
            </div>

            <div className="panel">
              <div className="form-group">
                <label className="form-label">Semantic Memory Vector Search</label>
                <div style={{ display: "flex", gap: "0.75rem" }}>
                  <input
                    className="form-input"
                    placeholder="e.g. Database connection pool exhaustion during high traffic spike..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && runMemorySearch()}
                  />
                  <button className="btn-primary" style={{ whiteSpace: "nowrap" }} onClick={runMemorySearch} disabled={memoryLoading}>
                    {memoryLoading ? "Searching Vectors..." : "Search RAG Memory"}
                  </button>
                </div>
              </div>
            </div>

            {patternsData && (
              <div className="grid-2" style={{ marginBottom: "1.5rem" }}>
                <div className="panel" style={{ background: "rgba(17, 24, 39, 0.9)" }}>
                  <div className="panel-header">
                    <h3 className="panel-title">Knowledge Base Memory Stats</h3>
                  </div>
                  <div style={{ display: "flex", gap: "2rem", marginTop: "0.5rem" }}>
                    <div>
                      <div style={{ fontSize: "1.75rem", fontWeight: "800", color: "#6366f1" }}>
                        {patternsData.total_incidents}
                      </div>
                      <div style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>Stored Incidents</div>
                    </div>
                    <div>
                      <div style={{ fontSize: "1.75rem", fontWeight: "800", color: "#f43f5e" }}>
                        {patternsData.patterns?.length || 0}
                      </div>
                      <div style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>Recurring Risk Trends</div>
                    </div>
                  </div>
                </div>

                <div className="panel" style={{ background: "rgba(17, 24, 39, 0.9)" }}>
                  <div className="panel-header">
                    <h3 className="panel-title">Failure Category Distribution</h3>
                  </div>
                  <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", marginTop: "0.5rem" }}>
                    {Object.entries(patternsData.category_counts || {}).map(([cat, count], i) => (
                      count > 0 && (
                        <div key={i} className="diff-tag" style={{ background: "rgba(99, 102, 241, 0.15)", color: "#a5b4fc", padding: "0.4rem 0.75rem" }}>
                          <strong>{cat}:</strong> {count}
                        </div>
                      )
                    ))}
                  </div>
                </div>
              </div>
            )}

            <h3 style={{ fontSize: "1.2rem", fontWeight: "700", marginBottom: "1rem" }}>
              Semantic Vector Search Results ({searchResults.length})
            </h3>

            {searchResults.map((item, idx) => (
              <div key={idx} className="commit-card" style={{ borderLeft: "4px solid #6366f1" }}>
                <div className="commit-header">
                  <div>
                    <span className="diff-tag" style={{ background: "rgba(99, 102, 241, 0.2)", color: "#818cf8" }}>
                      {item.service} Service
                    </span>
                    <span className="diff-tag">{item.error_type}</span>
                  </div>
                  <div className="badge-confidence low" style={{ background: "rgba(99, 102, 241, 0.15)", color: "#818cf8", borderColor: "rgba(99, 102, 241, 0.3)" }}>
                    <span>{item.similarity_score}% Vector Similarity</span>
                  </div>
                </div>

                <div className="commit-msg" style={{ marginTop: "0.5rem" }}>{item.summary}</div>

                <div className="grid-2" style={{ marginTop: "0.75rem" }}>
                  <div className="ai-box" style={{ borderLeftColor: "#f43f5e" }}>
                    <div className="ai-box-title" style={{ color: "#f43f5e" }}>Historical Root Cause</div>
                    <div style={{ fontSize: "0.875rem" }}>{item.root_cause}</div>
                  </div>

                  <div className="ai-box" style={{ borderLeftColor: "#10b981" }}>
                    <div className="ai-box-title" style={{ color: "#10b981" }}>Proven Resolution</div>
                    <div style={{ fontSize: "0.875rem" }}>{item.resolution}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* TAB 4: Prevention Engine */}
        {activeTab === "prevention" && (
          <div>
            <div className="page-header">
              <h1 className="page-title">Prevention Intelligence Engine</h1>
              <p className="page-subtitle">
                Transform incident analysis into proactive preventative action: generate Pytest regression tests, Prometheus alert rules, operational runbooks, and architecture recommendations.
              </p>
            </div>

            <div className="panel">
              <div className="grid-2">
                <div className="form-group">
                  <label className="form-label">Incident Summary</label>
                  <input
                    className="form-input"
                    value={prevSummary}
                    onChange={(e) => setPrevSummary(e.target.value)}
                    placeholder="e.g. Database connection pool exhaustion during flash sale"
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Failure Category</label>
                  <select
                    className="form-input"
                    value={prevCategory}
                    onChange={(e) => setPrevCategory(e.target.value)}
                  >
                    <option value="Database">Database & Storage</option>
                    <option value="Authentication">Authentication & JWT</option>
                    <option value="Networking">Networking & Gateway</option>
                    <option value="Configuration">Configuration & Env</option>
                    <option value="Caching">Caching & Redis</option>
                    <option value="API">API Endpoints</option>
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Target Root Cause</label>
                <textarea
                  className="form-textarea"
                  rows="3"
                  value={prevRootCause}
                  onChange={(e) => setPrevRootCause(e.target.value)}
                  placeholder="Describe root cause to generate targeted prevention artifacts..."
                />
              </div>

              <button
                className="btn-primary"
                style={{ background: "linear-gradient(135deg, #a855f7 0%, #6366f1 100%)" }}
                onClick={generatePreventionPackage}
                disabled={preventionLoading}
              >
                {preventionLoading ? "Generating Prevention Package & Validating Artifacts..." : "Generate Prevention Package"}
              </button>
            </div>

            {preventionPkg && (
              <div>
                <div className="panel-header" style={{ marginBottom: "1rem" }}>
                  <div style={{ display: "flex", gap: "0.5rem" }}>
                    <button
                      className={`nav-tab ${artifactTab === "test" ? "active" : ""}`}
                      onClick={() => setArtifactTab("test")}
                    >
                      Pytest Test
                    </button>
                    <button
                      className={`nav-tab ${artifactTab === "alert" ? "active" : ""}`}
                      onClick={() => setArtifactTab("alert")}
                    >
                      Prometheus Alerts
                    </button>
                    <button
                      className={`nav-tab ${artifactTab === "runbook" ? "active" : ""}`}
                      onClick={() => setArtifactTab("runbook")}
                    >
                      SRE Runbook
                    </button>
                    <button
                      className={`nav-tab ${artifactTab === "rec" ? "active" : ""}`}
                      onClick={() => setArtifactTab("rec")}
                    >
                      Architecture Recommendation
                    </button>
                  </div>

                  <button className="btn-primary" style={{ padding: "0.5rem 1rem", fontSize: "0.85rem" }} onClick={downloadPackage}>
                    Download Package JSON
                  </button>
                </div>

                {artifactTab === "test" && (
                  <div className="panel">
                    <div className="panel-header">
                      <h3 className="panel-title">Generated Pytest Regression Test</h3>
                      <span className="diff-tag" style={{ background: "rgba(16, 185, 129, 0.2)", color: "#34d399" }}>
                        Validated (Contains Assertions)
                      </span>
                    </div>
                    <pre className="diff-container" style={{ maxHeight: "none" }}>{preventionPkg.test_code}</pre>
                  </div>
                )}

                {artifactTab === "alert" && (
                  <div className="panel">
                    <div className="panel-header">
                      <h3 className="panel-title">Prometheus & Grafana Monitoring Alert Rules</h3>
                      <span className="diff-tag" style={{ background: "rgba(16, 185, 129, 0.2)", color: "#34d399" }}>
                        Validated Rule Metrics
                      </span>
                    </div>
                    <pre className="diff-container" style={{ maxHeight: "none" }}>{preventionPkg.alert_rules}</pre>
                  </div>
                )}

                {artifactTab === "runbook" && (
                  <div className="panel">
                    <div className="panel-header">
                      <h3 className="panel-title">SRE Operational Response Runbook</h3>
                      <span className="diff-tag" style={{ background: "rgba(16, 185, 129, 0.2)", color: "#34d399" }}>
                        SRE Standard Validated
                      </span>
                    </div>
                    <pre className="diff-container" style={{ maxHeight: "none", whiteSpace: "pre-wrap" }}>{preventionPkg.runbook}</pre>
                  </div>
                )}

                {artifactTab === "rec" && preventionPkg.architecture_recommendation && (
                  <div className="panel" style={{ borderLeft: "4px solid #a855f7" }}>
                    <div className="panel-header">
                      <div>
                        <h3 className="panel-title" style={{ fontSize: "1.2rem", color: "#c084fc" }}>
                          {preventionPkg.architecture_recommendation.title}
                        </h3>
                        <div style={{ fontSize: "0.85rem", color: "var(--text-muted)", marginTop: "0.25rem" }}>
                          Priority: <strong style={{ color: "#f43f5e" }}>{preventionPkg.architecture_recommendation.priority}</strong> (Risk Reduction Score: {preventionPkg.architecture_recommendation.score}/100)
                        </div>
                      </div>
                    </div>

                    <p style={{ marginTop: "0.75rem", marginBottom: "1rem", color: "var(--text-main)" }}>
                      {preventionPkg.architecture_recommendation.description}
                    </p>

                    <h4 style={{ fontSize: "0.9rem", color: "#818cf8", marginBottom: "0.5rem" }}>Recommended Action Items:</h4>
                    <ul style={{ paddingLeft: "1.5rem" }}>
                      {preventionPkg.architecture_recommendation.action_items?.map((item, idx) => (
                        <li key={idx} style={{ marginBottom: "0.4rem" }}>{item}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* TAB 5: Reliability Analytics & Enterprise Integrations */}
        {activeTab === "analytics" && (
          <div>
            <div className="page-header">
              <h1 className="page-title">Enterprise Reliability Analytics & Integrations</h1>
              <p className="page-subtitle">
                Executive operational health metrics, MTTR/MTBF tracking, microservice risk indices, and live Jira/Slack integrations.
              </p>
            </div>

            {/* KPI Metrics Header Cards */}
            {analyticsData && (
              <div className="grid-2" style={{ gridTemplateColumns: "1fr 1fr 1fr", marginBottom: "1.5rem" }}>
                <div className="panel" style={{ textAlign: "center", background: "rgba(17, 24, 39, 0.95)" }}>
                  <div style={{ fontSize: "2.2rem", fontWeight: "800", color: "#818cf8" }}>
                    {analyticsData.mttr_minutes} mins
                  </div>
                  <div style={{ color: "var(--text-muted)", fontSize: "0.8rem", textTransform: "uppercase", letterSpacing: "0.05em" }}>
                    Mean Time To Resolution (MTTR)
                  </div>
                </div>

                <div className="panel" style={{ textAlign: "center", background: "rgba(17, 24, 39, 0.95)" }}>
                  <div style={{ fontSize: "2.2rem", fontWeight: "800", color: "#10b981" }}>
                    {analyticsData.system_availability}%
                  </div>
                  <div style={{ color: "var(--text-muted)", fontSize: "0.8rem", textTransform: "uppercase", letterSpacing: "0.05em" }}>
                    SLA Availability Target
                  </div>
                </div>

                <div className="panel" style={{ textAlign: "center", background: "rgba(17, 24, 39, 0.95)" }}>
                  <div style={{ fontSize: "2.2rem", fontWeight: "800", color: "#34d399" }}>
                    {analyticsData.technical_debt_index?.score}/100
                  </div>
                  <div style={{ color: "var(--text-muted)", fontSize: "0.8rem", textTransform: "uppercase", letterSpacing: "0.05em" }}>
                    Tech Debt Risk ({analyticsData.technical_debt_index?.rating})
                  </div>
                </div>
              </div>
            )}

            {/* Integrations Hub */}
            <div className="panel" style={{ borderLeft: "4px solid #10b981" }}>
              <div className="panel-header">
                <h3 className="panel-title">Enterprise Integrations Hub</h3>
                <span className="diff-tag" style={{ background: "rgba(16, 185, 129, 0.2)", color: "#34d399" }}>
                  Live API Integrations Ready
                </span>
              </div>

              <p style={{ fontSize: "0.9rem", color: "var(--text-muted)", marginBottom: "1rem" }}>
                Seamlessly push postmortem action items to Jira tickets and broadcast incident alerts to Slack channels.
              </p>

              <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
                <button
                  className="btn-primary"
                  style={{ background: "#2563eb" }}
                  onClick={triggerJiraIntegration}
                >
                  Auto-Generate Jira Ticket
                </button>

                <button
                  className="btn-primary"
                  style={{ background: "#4a154b" }}
                  onClick={triggerSlackIntegration}
                >
                  Broadcast Slack Block Kit Alert
                </button>
              </div>

              {/* Jira Notice Response */}
              {jiraNotice && (
                <div className="ai-box" style={{ borderLeftColor: "#2563eb", marginTop: "1rem" }}>
                  <div className="ai-box-title" style={{ color: "#60a5fa" }}>Jira REST API Integration Result</div>
                  <div><strong>{jiraNotice.message}</strong></div>
                  <div style={{ fontSize: "0.8rem", color: "var(--text-muted)", marginTop: "0.25rem" }}>
                    Target URL: <code>{jiraNotice.payload?.jira_url}</code> | Priority: {jiraNotice.payload?.fields?.priority?.name}
                  </div>
                </div>
              )}

              {/* Slack Notice Response */}
              {slackNotice && (
                <div className="ai-box" style={{ borderLeftColor: "#4a154b", marginTop: "1rem" }}>
                  <div className="ai-box-title" style={{ color: "#e879f9" }}>Slack Block Kit Integration Result</div>
                  <div><strong>{slackNotice.message}</strong></div>
                  <div style={{ fontSize: "0.8rem", color: "var(--text-muted)", marginTop: "0.25rem" }}>
                    Broadcast Channel: <code>{slackNotice.payload?.channel}</code> | Blocks Generated: {slackNotice.payload?.blocks?.length}
                  </div>
                </div>
              )}
            </div>

            {/* Microservice Operational Health Table */}
            {analyticsData && (
              <div className="panel">
                <div className="panel-header">
                  <h3 className="panel-title">Microservice Operational Health & MTTR</h3>
                </div>

                <div style={{ overflowX: "auto" }}>
                  <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "left", fontSize: "0.9rem" }}>
                    <thead>
                      <tr style={{ borderBottom: "1px solid var(--border-color)", color: "var(--text-muted)" }}>
                        <th style={{ padding: "0.75rem 1rem" }}>Service Name</th>
                        <th style={{ padding: "0.75rem 1rem" }}>Status</th>
                        <th style={{ padding: "0.75rem 1rem" }}>MTTR</th>
                        <th style={{ padding: "0.75rem 1rem" }}>30-Day Incidents</th>
                        <th style={{ padding: "0.75rem 1rem" }}>Risk Rating</th>
                      </tr>
                    </thead>
                    <tbody>
                      {analyticsData.service_health?.map((svc, i) => (
                        <tr key={i} style={{ borderBottom: "1px solid rgba(255, 255, 255, 0.05)" }}>
                          <td style={{ padding: "0.75rem 1rem", fontWeight: "600" }}>{svc.name}</td>
                          <td style={{ padding: "0.75rem 1rem" }}>
                            <span className="diff-tag" style={{ background: svc.status === "Healthy" ? "rgba(16, 185, 129, 0.2)" : "rgba(245, 158, 11, 0.2)", color: svc.status === "Healthy" ? "#34d399" : "#fbbf24" }}>
                              {svc.status}
                            </span>
                          </td>
                          <td style={{ padding: "0.75rem 1rem" }}>{svc.mttr}</td>
                          <td style={{ padding: "0.75rem 1rem" }}>{svc.incidents_30d}</td>
                          <td style={{ padding: "0.75rem 1rem" }}>
                            <strong style={{ color: svc.risk_score === "Low" ? "#10b981" : "#f59e0b" }}>
                              {svc.risk_score} Risk
                            </strong>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;