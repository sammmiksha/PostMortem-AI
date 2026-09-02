from ollama import chat
import json


class LLMService:

    def generate(self, prompt: str) -> str:
        try:
            response = chat(
                model="qwen2.5:3b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                format="json"
            )
            return response["message"]["content"]
        except Exception as e:
            print(f"Error invoking Ollama: {e}")
            return json.dumps({
                "confidence": 50,
                "reason": "AI Service unavailable or failed to process commit diff.",
                "evidence": ["Error during AI processing"],
                "alternatives": []
            })

    def analyze_incident(self, incident_details: str):
        prompt = f"""
You are a Senior Site Reliability Engineer.

Analyze the incident.

Return ONLY valid JSON.

DO NOT return explanations.
DO NOT return markdown.
DO NOT return code fences.

Required schema:

{{
    "summary": "string",
    "root_cause": "string",
    "impact": "string",
    "recommendations": [
        "string"
    ]
}}

Incident:
{incident_details}
"""

        response = chat(
            model="qwen2.5:3b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            format="json"
        )

        content = response["message"]["content"]

        try:
            return json.loads(content)

        except Exception:
            return {
                "summary": "Failed to parse model output",
                "root_cause": "",
                "impact": "",
                "recommendations": []
            }