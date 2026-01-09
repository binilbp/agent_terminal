# this file contains the functions for setting up llm

# this list shows the different available run types
available_run_types = ['groq', 'ollama']



from dataclasses import replace
from config.settings import Settings

def set_run_type(settings: Settings) -> Settings:

    count = 1
    print("Run Types Available: ")
    for type in available_run_types:
        print(f'{count}. {type}')
        count+=1

    #setting the value and handling the invalid input
    try:
        option_number = int(input("Enter Option Number: "))
        selected_run_type = available_run_types[option_number - 1]
        settings = replace(settings, run_type = selected_run_type)
        print(f'[INFO]: set run type as {available_run_types[option_number-1]}')

    except:
        print(f"[ERROR]: invalid option")
        settings = replace(settings, run_type = available_run_types[0])
        print(f"[INFO]: default value ({available_run_types[0]}) selected")

     
    return settings



