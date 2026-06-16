PART 2 IMPLEMENTATION DOCUMENT
Git Root Cause Analyzer
Mission

Transform the project from:

AI analyzes incidents

to

AI analyzes incidents
+
AI investigates repository history
+
AI identifies likely responsible commits

This is the first feature that makes the project genuinely different from a simple AI postmortem generator.

Success Criteria

At the end of Part 2:

User provides:

Incident
Logs
Stack Trace
Repository

System returns:

Top suspicious commits

Confidence scores

Authors

Commit messages

AI explanation

Example:

Potential Root Cause

Commit:
a8f71bc

Author:
John Doe

Confidence:
84%

Reason:
Introduced retry logic that can cause connection exhaustion.
What We Are NOT Building

Do NOT build:

GitHub integration
Jira
Slack
RAG
Vector search
Embeddings
Prevention engine

Only repository analysis.

Part 2 Architecture
Incident

    │

    ▼

Stack Trace Parser

    │

    ▼

Git Analyzer

    │

    ▼

Commit Ranking Engine

    │

    ▼

AI Commit Reviewer

    │

    ▼

Suspicious Commit Report
PHASE 1
Repository Intelligence Layer
Goal

Allow system to understand repository history.

Install Dependencies
pip install GitPython

pip install pygit2

Use GitPython first.

Only add pygit2 later if needed.

Folder Structure

Create:

backend/

app/

services/

git/

├── git_service.py

├── commit_analyzer.py

├── ranking_engine.py

├── stacktrace_parser.py

├── diff_processor.py
PHASE 2
Git Service
Goal

Create reusable Git operations.

File
git_service.py
Required Functions
Clone Repository
clone_repo()
Open Repository
load_repo()
Recent Commits
get_recent_commits()
Commit Details
get_commit()
File History
get_file_history()
Commit Diff
get_diff()
Commit Author
get_author()
Blame Analysis
git_blame()
Deliverable

System can inspect repository history.

PHASE 3
Stack Trace Parser
Goal

Extract useful clues.

Input:

Traceback

payment.py

line 245

ConnectionTimeoutError

Output:

{
 "file":"payment.py",
 "line":245,
 "error":"ConnectionTimeoutError"
}
Extract
Error Type

Example:

ValueError
KeyError
TimeoutError
File Name

Example:

payment.py
Function Name

Example:

process_payment()
Line Number

Example:

245
Deliverable

Incident data becomes machine-readable.

PHASE 4
Commit Candidate Collection
Goal

Find commits that may have caused issue.

For affected file:

payment.py

Collect:

Last 50 commits

Touching:

payment.py

Store:

{
 "hash":"",
 "message":"",
 "author":"",
 "date":""
}
Ranking Factors

Each commit gets score.

Factor 1

File Match

Touched file

+40 points
Factor 2

Recentness

Last 7 days

+20
Factor 3

Keyword Similarity

Error:

timeout

Commit:

improved timeout handling

Score increases.

Factor 4

Function Match

Stack trace:

process_payment()

Commit modified:

process_payment()

High score.

Deliverable

Top suspicious commits.

PHASE 5
Commit Ranking Engine
Goal

Convert candidates into probabilities.

Create:

rank_commit()

Example Output

{
 "commit":"a82f31",
 "score":87
}

Store:

commit_analysis

Schema:

CREATE TABLE commit_analysis
(
 id UUID PRIMARY KEY,

 incident_id UUID,

 commit_hash TEXT,

 confidence INTEGER,

 explanation TEXT
);
PHASE 6
Diff Intelligence
Goal

Analyze code changes.

Input:

- timeout=5
+ timeout=30

Extract:

Configuration Change

Input:

Added DB pooling logic

Extract:

Database Modification

Categories:

Database

Authentication

API

Configuration

Caching

Deployment

Networking
Deliverable

Commits become understandable.

PHASE 7
AI Commit Reviewer
Goal

Use AI to reason about commit relevance.

Input to AI:

Incident Summary

Stack Trace

Commit Message

Commit Diff

Affected Files

Prompt

You are a senior software engineer.

Analyze whether this commit could have caused the incident.

Provide:

1. Confidence score

2. Explanation

3. Supporting evidence

4. Alternative explanations

Expected Output

{
 "confidence":84,
 "reason":"Modified retry logic."
}
PHASE 8
Database Changes

New Tables

commits
CREATE TABLE commits
(
 id UUID PRIMARY KEY,

 hash TEXT,

 author TEXT,

 message TEXT,

 commit_date TIMESTAMP
);
commit_analysis
CREATE TABLE commit_analysis
(
 id UUID PRIMARY KEY,

 incident_id UUID,

 commit_hash TEXT,

 confidence INTEGER,

 explanation TEXT
);
PHASE 9
API Layer

New Endpoint

POST

/api/root-cause

Input

{
 "incident_id":"123",
 "repo_path":"..."
}

Output

{
 "top_commits":[]
}
PHASE 10
Frontend

New Page

/root-cause

Sections

Incident

Show:

Summary
Candidate Commits

Show:

Commit Hash

Author

Score
AI Analysis

Show:

Reason
TESTING CHECKLIST

Before moving to Part 3:

Git Tests
 Repository loads correctly
 Commit history retrieved
 Diff extraction works
 Blame works
Ranking Tests
 File matching works
 Keyword scoring works
 Recentness scoring works
AI Tests
 Explanations generated
 Confidence scores generated
 Invalid outputs handled
API Tests
 Endpoint works
 Errors handled
 Invalid repositories handled
Definition Of Done

Only proceed to Part 3 if:

 Repository scanner complete
 Commit collector complete
 Stack trace parser complete
 Ranking engine complete
 AI reviewer complete
 Database schema updated
 API endpoint complete
 Frontend page complete
 Documentation written
 Tests passing