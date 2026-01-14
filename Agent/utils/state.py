# this file is used to define the state used by the agent


from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages
from typing import Literal


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    classification: Literal[
        "REQUIRES_LINUX_ASSISTANCE",
        "DOES_NOT_REQUIRE_LINUX_ASSISTANCE",
        "NEEDS_CLARIFICATION"
    ]
    classification_reason: str
    plan_list: list[str]
