from typing_extensions import TypedDict, Annotated

from langchain.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END

# class AgentState(TypedDict):
#     goal: str
#     command_generated: str
#     exit_code: int
#     user_approved: bool = False
#     sanity_check_passed: bool = False

llm = ChatOllama(model = "llama3.2", temperature=0)

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]









