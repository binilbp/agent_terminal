from config.settings import SETTINGS
from Agent.agent import run_agent

def main():
    # print(SETTINGS.classifier_llm.service)
    print(f'SETTINGS Applied:\n {SETTINGS.model_dump_json(indent=4)}\n')
    
    run_agent()


if __name__ == "__main__":
    main()
