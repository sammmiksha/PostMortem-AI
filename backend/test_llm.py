# test_llm.py

from app.services.llm_service import LLMService

llm = LLMService()

result = llm.analyze_incident(
    "Production PostgreSQL server became unavailable for 15 minutes causing API failures."
)

print(result)