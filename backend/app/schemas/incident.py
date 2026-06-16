from pydantic import BaseModel

class IncidentRequest(BaseModel):
    title: str
    incident_details: str