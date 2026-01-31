# this file contains all the schemas used by various nodes 
from pydantic import BaseModel, Field




from typing import Literal
from pydantic import BaseModel, Field


class ClassificationSchema(BaseModel):
    """
    Classification schema to determine whether a user query:
    - requires Linux shell/system assistance,
    - does not require it, or
    - needs clarification before taking action.
    """

    classification: Literal[
        "REQUIRES_LINUX_ASSISTANCE",
        "DOES_NOT_REQUIRE_LINUX_ASSISTANCE",
        "NEEDS_CLARIFICATION",
    ] = Field(
        description=(
            "Classification result:\n"
            "- REQUIRES_LINUX_ASSISTANCE: The task is explicit, unambiguous, and can be "
            "safely completed using Linux shell commands.\n"
            "- DOES_NOT_REQUIRE_LINUX_ASSISTANCE: The request is conceptual, informational, "
            "GUI-only, physical, or unrelated to system operations.\n"
            "- NEEDS_CLARIFICATION: The request is ambiguous, underspecified, or involves "
            "hardware/system setup with multiple possible paths (e.g., printer, Wi-Fi)."
        )
    )

    reasoning: str = Field(
        description=(
            "A brief explanation justifying the classification. "
            "Mention ambiguity, missing details, physical actions, or why shell commands "
            "are or are not appropriate."
        )
    )



class PlanListSchema(BaseModel):
    """
    The structural blueprint for the execution plan.    
    """

    plan_list: list[str] = Field(
        description="A list of atomic, linear execution steps.Each element should be a single string describing an action (e.g., ['update the apt', 'create a new file', 'find current working directory'])."
        )



class TerminalExecutable(BaseModel):
    """
    Check if the provided steps can be completed using a terminal
    """

    is_executable: bool = Field(
            description=(
                "True if each steps given can be completed using actual terminal commmands"
                "False if all steps cannot be completed using actual terminal commands"
            )
    )



class CommandGenerationSchema(BaseModel):
    """
    Command Generation instruction
    """

    command: str = Field(
            description=(
                "the shell command to be executed, provided as a plain string"
            )
    )

