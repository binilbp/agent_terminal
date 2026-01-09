# this file contains the base settings pydantic model and the functions to change the settings value

from pydantic import BaseModel, Field
from typing import Literal, get_args



class Settings(BaseModel):
    run_type: Literal['groq', 'ollama'] = 'groq'
    temperature: float = Field(default = 0.0, ge = 0.0, le = 1.0)
    max_retries: int = Field(default = 2, ge = 0, le = 4)


    model_config = {
        "frozen": True
    }



# modify the run type of the models
def set_run_type(settings: Settings) -> Settings:

    available_run_types = get_args(
            Settings.model_fields['run_type'].annotation
    )

    print("Run Types Available: ")
    for i, run_type in enumerate(available_run_types, start=1):
        print(f'{i}. {run_type}')

    #setting the value and handling the invalid input
    try:
        option_number = int(input("Enter Option Number: "))
        selected_run_type = available_run_types[option_number - 1]

        #create a new model since settings is immutable
        settings = settings.model_copy(
            update={'run_type': selected_run_type}
        )

        print(f'[INFO]: set run type as {available_run_types[option_number-1]}')

    except (ValueError, IndexError):
        print(f"[ERROR]: invalid option")
        settings = settings.model_copy(
            update={'run_type': available_run_types[0]}
        )        
        print(f"[INFO]: default value ({available_run_types[0]}) selected")

     
    return settings


