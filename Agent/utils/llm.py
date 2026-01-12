# this file contains llm setup functions, which return preconfigured llm runnables based on the settings values

from config.settings import SETTINGS 
from langchain_groq import ChatGroq

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


