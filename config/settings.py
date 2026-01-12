import json
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Literal

# load secrets from .env file
load_dotenv()


class LLMParams(BaseModel):
    #defining the possible services to user
    service: Literal["groq_api", "ollama" ] 
    model_name: str
    model_temp: float = Field(ge=0.0, le=2.0) # Temperature constraints
    max_retry: int = Field(default=2, ge=0)
    max_tokens: int = Field(default=300, gt=0, le=600)

class Settings(BaseModel):
    name: str
    classifier_llm: LLMParams
    command_gen_llm: LLMParams
    small_chat_llm: LLMParams
    
    # Internal validation logic
    @model_validator(mode='after')
    def check_api_keys_exist(self):

        # Check Classifier Service
        if self.classifier_llm.service == "groq_api" and not os.getenv("GROQ_API_KEY"):
            raise ValueError("Configuration asks for 'groq_api' in classifier_llm, but GROQ_API_KEY is missing in .env")
            
        # Check Command Gen Service
        if self.command_gen_llm.service == "groq_api" and not os.getenv("GROQ_API_KEY"):
            raise ValueError("Configuration asks for 'groq_api' in command_gen_llm, but GROQ_API_KEY is missing in .env")
            

        # Check Small Chat llm
        if self.command_gen_llm.service == "groq_api" and not os.getenv("GROQ_API_KEY"):
            raise ValueError("Configuration asks for 'groq_api' in command_gen_llm, but GROQ_API_KEY is missing in .env")

        return self


BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS_PATH = os.path.join(BASE_DIR, "config", "settings.json")

def load_settings() -> Settings:
    if not os.path.exists(SETTINGS_PATH):
        raise FileNotFoundError(f"settings.json missing at {SETTINGS_PATH}")

    with open(SETTINGS_PATH, "r") as f:
        data = json.load(f)

    try:
        # Pydantic validates types and runs the @model_validator above
        settings = Settings(**data)
        return settings
    except ValidationError as e:
        print("\n!!! CONFIGURATION ERROR !!!")
        print(f"Validation failed:\n{e}")
        # Exit or re-raise depending on preference
        raise

# Instantiate globally
SETTINGS = load_settings()
