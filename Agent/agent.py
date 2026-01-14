#this file contain the functions to run the agent 



from langchain_core.messages import HumanMessage
from Agent.graph import get_graph



graph = get_graph()



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


