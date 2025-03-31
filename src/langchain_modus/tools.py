from typing import Optional, Type
from langchain_core.tools import BaseTool
from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from .client import ModusClient
from .input_schemas import GetPredicatesInput, ValidateAssignmentInput
from typing import Any, Dict

class ModusBaseTool(BaseTool):
    """Base tool class for Modus operations"""
    client: ModusClient
    handle_tool_error: bool = True

    class Config:
        arbitrary_types_allowed = True

class GetPredicatesTool(ModusBaseTool):
    """Tool for fetching predicates from a Modus document"""
    name: str = "modus_get_predicates"
    description: str = (
        "Fetch available predicates from a Modus document. "
        "Useful for understanding what logical constraints exist."
    )
    args_schema: Type[GetPredicatesInput] = GetPredicatesInput

    def _run(
        self,
        project_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        try:
            return [{'alias': result['alias'], 'content': result['content']} for result in self.client.get_predicates(project_id)]
        except Exception as e:
            return {"error": str(e)}

    async def _arun(
        self,
        project_id: int,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        try:
            return await [{'alias': result['alias'], 'content': result['content']} for result in self.client.get_predicates(project_id)]
        except Exception as e:
            return {"error": str(e)}

class ValidateAssignmentTool(ModusBaseTool):
    """Tool for validating truth assignments against Modus logic"""
    name: str = "modus_validate_assignment"
    description: str = (
        "Validate truth assignments against a Modus document's logical constraints. "
        "Returns validation results and any failed implications."
    )
    args_schema: Type[ValidateAssignmentInput] = ValidateAssignmentInput

    def _run(
        self,
        project_id: str,
        assignments: Dict[str, bool],
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        try:
            return self.client.validate_assignment(project_id, assignments)
        except Exception as e:
            return {"error": str(e)}

    async def _arun(
        self,
        project_id: str,
        assignments: Dict[str, bool],
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Dict[str, Any]:
        try:
            return await self.client.avalidate_assignment(project_id, assignments)
        except Exception as e:
            return {"error": str(e)}

def create_modus_tools(api_key: str, base_url: Optional[str] = None) -> list[BaseTool]:
    """Factory function to create Modus tools with shared client"""
    client = ModusClient(api_key=api_key)
    if base_url:
        client.base_url = base_url
        
    return [
        GetPredicatesTool(client=client),
        ValidateAssignmentTool(client=client)
    ]
