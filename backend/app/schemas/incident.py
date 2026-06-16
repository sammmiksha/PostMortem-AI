from pydantic import BaseModel, Field

class IncidentRequest(BaseModel):

    title: str = Field(
        min_length=5,
        max_length=200
    )

    incident_details: str = Field(
        min_length=20,
        max_length=10000
    )