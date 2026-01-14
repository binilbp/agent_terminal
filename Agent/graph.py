# this file contains function to build the agent graph and return it



from langgraph.graph import StateGraph, START, END
from Agent.utils.state import AgentState 
from Agent.utils.nodes import classification, planning, out_of_scope, clarification, test_print_state



def get_graph():
    graph_builder = StateGraph(AgentState)
    graph_builder.add_node( "classification", classification )
    graph_builder.add_node( "planning", planning )
    graph_builder.add_node( "out_of_scope", out_of_scope )
    graph_builder.add_node( "clarification", clarification )


    graph_builder.add_edge( START, "classification" )
    graph_builder.add_edge( "clarification", "classification" )

    return graph_builder.compile()
