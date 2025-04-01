from pydantic import BaseModel, Field, Json
from typing import Dict

class GetPredicatesInput(BaseModel):
    """Input for GetPredicatesTool"""
    project_id: str = Field(..., description="ID of the project to fetch predicates for")  # Changed from document_id

class ValidateAssignmentInput(BaseModel):
    project_id: str = Field(..., description="Modus project ID")
    assignments: Json[Dict[str, bool]] = Field(
        ...,
        description="JSON string of truth assignments",
        example='{"RecentOrder": true, "DamagedProduct": false}'
    )
