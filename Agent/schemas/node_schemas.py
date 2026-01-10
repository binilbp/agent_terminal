# this file contains all the schemas used by various nodes 
from pydantic import BaseModel, Field



class SystemAssistSchema(BaseModel):
    """
    Classification schema to determine if a user query requires Linux system, 
    shell, or administrative assistance.
    """
    
    reasoning: str = Field(
        description=(
            "A brief analysis of the user query. Explain whether the query explicitly "
            "asks for Linux command-line execution, system configuration, "
            "file system manipulation, or troubleshooting."
        )
    )
    
    requires_linux_assistance: bool = Field(
        description=(
            "True if the query requires: "
            "1. Executing Shell/Bash commands. "
            "2. System Administration (permissions, users, processes). "
            "3. Network configuration (not just web browsing). "
            "4. File system operations (moving, deleting, grep, etc). "
            "False if the query is general coding (Python, JS), creative writing, "
            "or general knowledge."
        )
    )
