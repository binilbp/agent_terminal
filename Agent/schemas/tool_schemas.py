#this file contain all the schemas used by the existing tools
from pydantic import BaseModel, Field


class CommandSchema(BaseModel):
    """Schema to force the LLM to output ONLY the command."""
    command: str = Field(description="The pure linux shell command. No markdown, no explanations.")
