from config.settings import SETTINGS
from Agent.agent import run_agent

def main():
    # print(SETTINGS.classifier_llm.service)
    print(f'SETTINGS Applied:\n {SETTINGS.model_dump_json(indent=4)}\n')
    
    while True:
        user_input = input("\nUSER: ")

        #condition to break the while loop/ to exit
        if user_input.lower() in ["quit", "exit"]:
            break

        run_agent(user_input)


if __name__ == "__main__":
    main()
