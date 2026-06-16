from app.services.llm_service import LLMService

class ReportGenerator:

    def __init__(self):
        self.llm = LLMService()

    def generate(self, incident_details: str):
        return self.llm.analyze_incident(
            incident_details
        )