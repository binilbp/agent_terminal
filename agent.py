from typing_extensions import TypedDict, Annotated

# from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# class AgentState(TypedDict):
#     goal: str
#     command_generated: str
#     exit_code: int
#     user_approved: bool = False
#     sanity_check_passed: bool = False

big_llm = ChatOllama(model = "qwen2.5-coder:3b", temperature=0)

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# Nodes
def big_agent(state: AgentState):
    messages = state["messages"]

    response = big_llm.invoke(messages)

    return {"messages": [response]}


# Building the Graph
graph_builder = StateGraph(AgentState)

graph_builder.add_node("big_agent", big_agent)
graph_builder.add_edge(START, "big_agent")
graph_builder.add_edge("big_agent",END)

graph=graph_builder.compile()


# Loop Function
def run_agent():
    while True:
        user_input = input("User: ")

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
                        print("f Tool Called: {last_message.tool_calls[0]['name']} ")
                    else:
                        print(f"Agent: {last_message.content}")

                elif last_message.type == "tool":
                    print(f"Tool Output: {last_message.content}")

        

if __name__ == "__main__":
    run_agent()






