# this file contains the tool definitions usable by agent



from langchain_core.tools import tool



import subprocess 
@tool
def get_system_info() -> str:
    """Get system info"""
    info = subprocess.run(["hostnamectl"], capture_output=True)
    return info



@tool
def generate_command(query: str) -> str:
    """
    Generate a Linux shell command.
    Use this tool when the user asks for a specific terminal operation.
    
    Args:
        query: The user's request (e.g. "install calculator")
    """    
    prompt = f"return the command for executing the user query on ubuntu: {query}"

    print("[info]: command_gen_llm running...")
    command_output = command_gen_llm.invoke(prompt)
    return command_output.command

