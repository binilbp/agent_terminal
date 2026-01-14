# this file contains all the node definitions used by the langgraph
# nodes beggining with "test" are only used for test purposes

from Agent.utils.llm import get_llm
from Agent.utils.state import AgentState
from config.settings import SETTINGS
from typing import Literal

from langgraph.types import Command
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from pprint import pformat



# llms

classifier_llm = get_llm("classifier")
simple_chat_llm = get_llm("small_chat")
planner_llm = get_llm("planner")



# router node to decide if the user input is about linux assistance or not
def classification(state: AgentState) -> Command[Literal["planning", "out_of_scope", "clarification"]]: 

    
    if SETTINGS.debug:
        print(f'\n[STATE INFO]: {pformat(state)}\n')

    sys_message = SystemMessage(content ="""
        You are a decision engine for an autonomous Linux Shell Agent.
        Classify the user's request into exactly ONE category:
        1. REQUIRES_LINUX_ASSISTANCE
        2. DOES_NOT_REQUIRE_LINUX_ASSISTANCE
        3. NEEDS_CLARIFICATION
        Core question:
        Can this request be safely and unambiguously solved using Linux shell commands
        without additional user input, assumptions, or physical actions?
        Rules:
        REQUIRES_LINUX_ASSISTANCE if:
        - The task is explicit, CLI-solvable, and complete.
        - No physical interaction or missing details are involved.
        DOES_NOT_REQUIRE_LINUX_ASSISTANCE if:
        - The request is conceptual, informational, GUI-only, physical, or a greeting.
        - The user asks to write code but not execute it.
        NEEDS_CLARIFICATION if:
        - The request is underspecified or ambiguous.
        - It involves hardware or system setup with multiple possible paths
          (e.g., printers, Wi-Fi, Bluetooth, external devices).
        - Running commands would require assumptions.
        Output requirements:
        - classification: one of the three categories
        - reasoning: brief justification(if REQUIRES_LINUX_ASSISTANCE or DOES_NOT_REQUIRE_LINUX_ASSISTANCE ),problems (if NEED_CLARIFICATION)
        Do not provide commands or explanations.
   """)

    user_query = state["messages"]
    try:
        print("[INFO]: classification node running")

        message = [sys_message] + user_query
        result = classifier_llm.invoke(message)
        
        assist_required = result.classification
        reason = result.reasoning

        if assist_required == "REQUIRES_LINUX_ASSISTANCE":
            goto = "planning"
        elif assist_required == "DOES_NOT_REQUIRE_LINUX_ASSISTANCE":
            goto = "out_of_scope"
        else:
            goto = "clarification"

    except Exception as e:
        print("[WARN]: classifier failed, defaulting to False")
        print(e)

        assist_required = "DOES_NOT_REQUIRE_LINUX_ASSISTANCE"
        reason = "internal error"
        # just for graceful exit
        goto = "out_of_scope"

    # control flow to the next node
    return Command( 
        update = {
            'classification': assist_required,
            'classification_reason': reason
        },
        goto = goto,
    )



def out_of_scope(state: AgentState):
    
    if SETTINGS.debug:
        print(f'\n[STATE INFO]: {pformat(state)}\n')


    print(f'[INFO]: out of scope node running')

    reason = state["classification_reason"]
    #here user query is an item not a list; we taking the last element from the list
    user_query = state["messages"][-1]

    sys_message = SystemMessage(content=f"""
        You are {SETTINGS.name} a terminal assistant capable of helping with system command execution.
        Your instruction:
        For small talk, reply in under 15 words mentioning your readiness to assist. 
        For other requests, politely decline why you cant help with the request. reson:{reason}"""
    )    


    message = [sys_message, user_query ]
    result = simple_chat_llm.invoke(message)
    if SETTINGS.debug:
        print(f'[NODE]: {result.content}')

    return { "messages" : [result]}



def planning(state:AgentState):

    if SETTINGS.debug:
        print(f'\n[STATE INFO]: {pformat(state)}\n')


    print(f'[INFO]: planning node running')

    user_query = state["messages"][-1].content

    sys_message = SystemMessage(content = '''Role: You are a Senior Linux System Architect .
    Task: Analyze the user's request and break it down into a series of simple, atomic, linear steps that can executed using a shell.
    Output : Output the execution plan as a JSON object with a key "plan_list"
    Guidelines:
        Each step must be a single logical action (e.g., "Update apt packages", "Install Python3", "Create a file named hello.py").
        Ensure steps are in the correct dependency order.
        The steps should be possible on the current user system
        Do not include verification steps; the execution agent will handle verification.''')

    message = [sys_message, user_query]
    result =  planner_llm.invoke( message )
    print(f'[NODE]:Plan List: {result.plan_list}')

    return {"plan_list": [result.plan_list]}


def clarification(state: AgentState):
     
    if SETTINGS.debug:
        print(f'\n[STATE INFO]: {pformat(state)}\n')

    print(f'[INFO]: clarification node running')

    sys_message = SystemMessage(content = f'''
    You are a clarification engine for a Linux Shell Agent.
    you are duty is to prepare a question to clarify the issue to the user, so that user can respond back with more info
    ''')

    problem = state['classification_reason']
    result = simple_chat_llm.invoke([sys_message, f'issue:{problem}'])

    if SETTINGS.debug:
        print(f'[NODE]: {result.content}')

    user_input = input("[USER ]:")

    return {"messages": [result, HumanMessage(content = user_input)]}


from pprint import pformat
def test_print_state(state: AgentState):
    print(f'\n[TEST Node] :Current State: {pformat(state)}\n')
