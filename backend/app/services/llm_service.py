# services/llm_service.py
from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()

client = OpenAI(api_key="YOUR_KEY")

class LLMService:

    def analyze_incident(self, incident_details):

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role":"system",
                    "content":"You are an incident response expert."
                },
                {
                    "role":"user",
                    "content":incident_details
                }
            ]
        )

        return response.choices[0].message.content