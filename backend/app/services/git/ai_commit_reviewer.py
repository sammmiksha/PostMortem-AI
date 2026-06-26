import json
from app.services.ai.llm_service import LLMService  # Fixed import path based on your folder structure

class AICommitReviewer:

    def __init__(self):
        # Using LLMService since llm_service.pyc was noted in your backend files
        self.llm = LLMService()
        
    def build_prompt(self, incident: dict, stacktrace: dict, commit: dict) -> str:
        """Constructs the prompt securely with proper indentation context."""
        return f"""You are a senior software engineer.

Analyze whether this commit could have caused the incident.

Incident
{json.dumps(incident, indent=2)}

Stack Trace
{json.dumps(stacktrace, indent=2)}

Commit
Hash: {commit.get("hash")}
Message: {commit.get("message")}
Author: {commit.get("author")}
Score: {commit.get("score")}

Diff Analysis:
{json.dumps(commit.get("changes_diff"), indent=2)}

Return JSON only.
{{
    "confidence": 0,
    "reason": "",
    "evidence": [],
    "alternatives": []
}}"""

    def review_commit(self, incident: dict, stacktrace: dict, commit: dict) -> dict:
        """Sends context to the LLM and forces a structured payload return."""
        prompt = self.build_prompt(incident, stacktrace, commit)
        response = self.llm.generate(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback handling in case the model returns markdown code block wraps
            clean_response = response.strip().strip("```json").strip("```").strip()
            return json.loads(clean_response)