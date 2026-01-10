# this file contains all the node definitions used by the langgraph

from Agent.utils.llm import get_classifier_llm


# llms
classifier_llm = get_classifier_llm()



def is_sys_ass_req(state): 

    query = "find the nvidia driver version insalled"

    print("[INFO]: identifying user request type")
    result = classifier_llm.invoke(query)
    print(f'[AGENT]: {result}')


