from typing_extensions import TypedDict, Annotated
from pydantic import BaseModel, Field

from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq

from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


# Model Service selection
service = "GROQ"
#service = "OLLAMA"


# class AgentState(TypedDict):
#     goal: str
#     command_generated: str
#     exit_code: int
#     user_approved: bool = False
#     sanity_check_passed: bool = False



# Schemas
class LinuxCommand(BaseModel):
    """Schema to force the LLM to output ONLY the command."""
    command: str = Field(description="The pure linux shell command. No markdown, no explanations.")



# Tools
@tool
def generate_command(query: str) -> str:
    """
    Generate a Linux shell command.
    Use this tool when the user asks for a specific terminal operation.
    
    Args:
        query: The user's request (e.g. "install calculator")
    """    
    prompt = f"return the command for executing the user query on ubuntu: {query}"

    print("[info]: kutti llm running...")
    tool_output = structured_small_llm.invoke(prompt)
    return tool_output.command

tools_list = [generate_command]

# State Defining
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]



# Model Defining
if service == "GROQ":
    # API Key setup
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    if "GROQ_API_KEY" not in os.environ:
        print("GROQ API key not found or not setup")
        exit 

    else:
        big_llm = ChatGroq(
            model="qwen/qwen3-32b",
            # model="llama-3.1-8b-instant",
            temperature = 0,
            max_retries = 2,
        )
        structured_small_llm = big_llm.with_structured_output(LinuxCommand)

elif service == "OLLAMA":
    small_llm = ChatOllama(model = "qwen2.5-coder:3b", temperature=0)
    structured_small_llm = small_llm.with_structured_output(LinuxCommand)
    big_llm = ChatOllama(model = "llama3.1:8b", temperature=0)



# Tool Binding the llm
big_llm = big_llm.bind_tools(tools_list)



# Nodes
def big_agent(state: AgentState):
    messages = state["messages"]
    sys_message = SystemMessage(content="""
    You are a helpful assistant. 
        - If the user just says "hi" or converses normally, reply naturally. 
        - ONLY call the 'generate_command' tool if the user explicitly asks for a Linux terminal command.
    """)    
    print("[INFO]: paapa llm running...")
    response = big_llm.invoke([sys_message] + messages)
    return {"messages": [response]}



# Building the Graph
graph_builder = StateGraph(AgentState)
graph_builder.add_node("big_agent", big_agent)
graph_builder.add_node("tools", ToolNode(tools_list))

graph_builder.add_edge(START, "big_agent")
graph_builder.add_conditional_edges("big_agent",tools_condition)
graph_builder.add_edge("tools", "big_agent")

graph=graph_builder.compile()



# Loop Function
def run_agent():
    while True:
        user_input = input("\nUSER: ")

        #condition to break the while loop/ to exit
        if user_input.lower() in ["quit", "exit"]:
            break

        events = graph.stream(
                {"messages":[HumanMessage(content=user_input)]},
                stream_mode="values"
        )
       
        for event in events:
            if "messages" in event:
                last_message = event["messages"][-1]
                if last_message.type == "ai":
                    if last_message.tool_calls:
                        print(f"[INFO]: Tool Called: {last_message.tool_calls[0]['name']} ")
                    else:
                        print(f"\nAGENT: {last_message.content}\n")

                elif last_message.type == "tool":
                    print(f"[INFO]: Tool Output: {last_message.content}")

        

if __name__ == "__main__":
    run_agent()






