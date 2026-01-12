# this file is used to define the state used by the agent


from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages



class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    is_sys_ass_req: bool

