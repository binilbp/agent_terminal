# this file contain the functions to run the agent in simple cli 
# for TUI use python main.py



from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from Agent.graph import get_graph
from config.settings import SETTINGS


graph = get_graph()


def run_cli_agent():
    print(SETTINGS.classifier_llm.service)
    if SETTINGS.debug:
        print(f'SETTINGS Applied:\n {SETTINGS.model_dump_json(indent=4)}\n')

    print("Linquix Backend")
    print("Type 'exit' for quit")

    config: RunnableConfig = {"configurable": {"thread_id": "session_1"}}

    while True:
        user_input = input("\nUSER: ")

        #condition to break the while loop/ to exit
        if user_input.lower() in ["quit", "exit"]:
            break

        events = graph.stream(
                    {"messages":[HumanMessage(content=user_input)]},
                    stream_mode="values",
                    config = config
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


