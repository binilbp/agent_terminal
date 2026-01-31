# this file contains function to build the agent graph and return it



from langgraph.graph import StateGraph, START, END
from Agent.utils.state import AgentState 
from Agent.utils.nodes import classification, planning, out_of_scope, clarification, test_print_state, supervisor, command_generation, execution
from langgraph.checkpoint.memory import MemorySaver



def get_graph():
    graph_builder = StateGraph(AgentState)
    graph_builder.add_node( "classification", classification )
    graph_builder.add_node( "planning", planning )
    graph_builder.add_node( "out_of_scope", out_of_scope )
    graph_builder.add_node( "clarification", clarification )
    graph_builder.add_node( "supervisor", supervisor )
    graph_builder.add_node( "command_generation", command_generation )
    graph_builder.add_node( "execution", execution )

    graph_builder.add_edge( START, "classification" )
    graph_builder.add_edge( "planning", "supervisor")
    graph_builder.add_edge( "command_generation", "supervisor" )
    graph_builder.add_edge( "execution", END)

    memory = MemorySaver()
    return graph_builder.compile(checkpointer=memory)
