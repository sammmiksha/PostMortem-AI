from app.services.git.commit_analyzer import CommitAnalyzer

trace = """
Traceback (most recent call last):
  File "backend/app/main.py", line 21, in analyze_incident
    report = generator.generate(request.incident_details)
RuntimeError: ConnectionTimeoutError: Failed to connect to PostgreSQL database pool at port 2907
"""

analyzer = CommitAnalyzer(r"C:\projects\PostMortem-AI")
result = analyzer.analyze(trace, incident_summary="DB pool connection timeout", limit_output=3, run_ai=False)
print("=== Parsed Stack Trace ===")
print(result["stacktrace"])
print("\n=== Top Candidate Commits ===")
for c in result["candidate_commits"]:
    print(f"Hash: {c['hash'][:8]} | Author: {c['author']} | Score: {c['score']}")
    print(f"  Msg: {c['message']}")
    print(f"  Reasons: {c['reasons']}")
