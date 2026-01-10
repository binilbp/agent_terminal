from config.settings import SETTINGS
from Agent.utils.state import AgentState

def main():
    # print(SETTINGS.classifier_llm.service)
    print(SETTINGS)
    
    from Agent.utils.nodes import is_sys_ass_req
    is_sys_ass_req(AgentState)


if __name__ == "__main__":
    main()
