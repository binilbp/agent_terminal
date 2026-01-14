# this file contains llm setup functions, which return preconfigured llm runnables based on the settings values

from config.settings import SETTINGS 
from langchain_groq import ChatGroq



# unified function to call other functions in this file 
def get_llm(llm):
    match llm:
        case "classifier":
            return get_classifier_llm()

        case "small_chat":
            return get_small_chat_llm()

        case "planner":
            return get_planner_llm()



def get_classifier_llm():
    
    if SETTINGS.classifier_llm.service == "groq_api":

        base_model = ChatGroq(
            model=SETTINGS.classifier_llm.model_name,
            temperature = SETTINGS.classifier_llm.model_temp,
            max_retries = SETTINGS.classifier_llm.max_retry,
            #max_tokens = 
        )

        # making classifier llm structured based on schema
        from Agent.schemas.node_schemas import SystemAssistSchema
        structured_model = base_model.with_structured_output(SystemAssistSchema)

        return structured_model



def get_small_chat_llm():
    
    if SETTINGS.classifier_llm.service == "groq_api":

        base_model = ChatGroq(
            model=SETTINGS.small_chat_llm.model_name,
            temperature = SETTINGS.small_chat_llm.model_temp,
            max_retries = SETTINGS.small_chat_llm.max_retry,
            max_tokens = SETTINGS.small_chat_llm.max_tokens
        )

        return base_model



from Agent.utils.tools import get_system_info
def get_planner_llm():
    
    if SETTINGS.classifier_llm.service == "groq_api":

        base_model = ChatGroq(
            model=SETTINGS.planner_llm.model_name,
            temperature = SETTINGS.planner_llm.model_temp,
            max_retries = SETTINGS.planner_llm.max_retry,
            max_tokens = SETTINGS.planner_llm.max_tokens
        )

        # from Agent.schemas.node_schemas import PlanListSchema
        # structured_model = base_model.with_structured_output(PlanListSchema, method="json_mode")
        # making the tool available for the model
        # model_with_tools = structured_model.bind_tools([get_system_info])

        return base_model

# ###### todo use match to set all to single functiono call, give is_executable llm

