from dataclasses import dataclass


# this provides a structure and default values  settings 


@dataclass(frozen=True)
class Settings:
    run_type: str = 'groq'
    temperature: float = 0
    max_retries: int = 2
