# this file contains the functions for setting up llm

# this list shows the different available run types


from config.settings import Settings
from typing import get_args

def set_run_type(settings: Settings) -> Settings:

    available_run_types = Settings.model_fields['run_types'].annotation

    print("Run Types Available: ")
    for i, type in enumerate(available_run_types, start=1):
        print(f'{i}. {type}')

    #setting the value and handling the invalid input
    try:
        option_number = int(input("Enter Option Number: "))
        selected_run_type = available_run_types[option_number - 1]
        #create a new model since settings is immutable
        settings = settings.model_copy(
            update('run_type': selected_run_type)
        )
        print(f'[INFO]: set run type as {available_run_types[option_number-1]}')

    except:
        print(f"[ERROR]: invalid option")
        settings = replace(settings, run_type = available_run_types[0])
        print(f"[INFO]: default value ({available_run_types[0]}) selected")

     
    return settings



