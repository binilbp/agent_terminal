# this file contains all the node definitions used by the langgraph
# nodes beggining with "test" are only used for test purposes

from Agent.utils.llm import get_classifier_llm, get_small_chat_llm
from Agent.utils.state import AgentState
from config.settings import SETTINGS
from typing import Literal

from langgraph.types import Command
from langchain_core.messages import SystemMessage, HumanMessage
from pprint import pformat



# llms
classifier_llm = get_classifier_llm()
small_chat_llm = get_small_chat_llm()



# router node to decide if the user input is about linux assistance or not
def is_sys_ass_req(state: AgentState) -> Command[Literal["planner", "retry"]]: 

    print(f'[STATE INFO]: \n{pformat(state)}')

    query = state["messages"][-1].content 
    try:
        print("[INFO]: is_sys_ass_req node running")
        result = classifier_llm.invoke(query)
        print(f'[AGENT]: {result}')
        assist_required = result.requires_linux_assistance
        if assist_required:
            goto = "planner"
        else:
            goto = "retry"

    except Exception as e:
        print("[WARN]: classifier failed, defaulting to False")
        print(e)
        assist_required = False
        goto = "retry"

    # control flow to the next node
    return Command( 
        update = {'is_sys_ass_req': assist_required},
        goto = goto,
    )



def retry(state: AgentState):
    
    print(f'\n[STATE INFO]: \n{pformat(state)}')

    # HumanMessage(content =......)
    user_query = state["messages"][-1].content

    sys_message = SystemMessage(content=f"""
        You are {SETTINGS.name} a terminal assistant capable of helping with system command execution.

        Your instruction:
        If it is a simple talk give appropriate simple reply in 10 words which also includes your assist ability, else reply in exactly one polite sentence acknowledging that you cannot help with the request and ask the user to try a possible specific Linux terminal assistance instead.""")
    
    message = [sys_message, user_query]
    result = small_chat_llm.invoke(message)
    print(f'[AGENT]: {result.content}')



def planner(state:AgentState):
    print(f'[INFO]: planner node running')




from pprint import pformat
def test_print_state(state: AgentState):
    print(f'\nCurrent State: {pformat(state)}\n')
