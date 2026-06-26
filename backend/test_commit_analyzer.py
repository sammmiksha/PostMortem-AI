from app.services.git.commit_analyzer import CommitAnalyzer

trace = """
Traceback (most recent call last):
  File "backend/app/main.py", line 42, in startup
    RuntimeError: Failed to initialize database
"""

analyzer = CommitAnalyzer(r"C:\projects\PostMortem-AI")
result = analyzer.analyze(trace)
print(result)