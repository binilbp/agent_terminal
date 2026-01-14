from config.settings import SETTINGS
from Agent.agent import run_agent

def main():
    # print(SETTINGS.classifier_llm.service)
    if SETTINGS.debug:
        print(f'SETTINGS Applied:\n {SETTINGS.model_dump_json(indent=4)}\n')
    
    print("Linquix Backend")
    print("Type 'exit' for quit")
    run_agent()


if __name__ == "__main__":
    main()
