from pydantic import BaseModel, Field
from typing import Dict

class GetPredicatesInput(BaseModel):
    """Input for GetPredicatesTool"""
    project_id: str = Field(..., description="ID of the project to fetch predicates for")  # Changed from document_id

class ValidateAssignmentInput(BaseModel):
    """Input for ValidateAssignmentTool"""
    project_id: str = Field(..., description="ID of the project to validate")  # Changed from document_id
    assignments: Dict[str, bool] = Field(
        ..., 
        description="Dictionary of truth assignments for predicates"
    )
