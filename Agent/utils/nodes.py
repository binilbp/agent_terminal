# this file contains all the node definitions used by the langgraph
# nodes beggining with "test" are only used for test purposes

from Agent.utils.llm import get_classifier_llm
from Agent.utils.state import AgentState
from pprint import pformat



# llms
classifier_llm = get_classifier_llm()



def is_sys_ass_req(state: AgentState): 

    query = state["messages"] 
    try:
        print(f'[STATE INFO]: \n{pformat(state)}')

        print("[INFO]: identifying user request type")
        result = classifier_llm.invoke(query)
        print(f'[AGENT]: {result}')
        
        return { 'is_sys_ass_req': result.requires_linux_assistance }
    except Exception as e:
        print("[WARN]: classifier failed, defaulting to False")
        print(e)
        return { 'is_sys_ass_req': False}



from pprint import pformat
def test_print_state(state: AgentState):
    print(f'\nCurrent State: {pformat(state)}\n')
