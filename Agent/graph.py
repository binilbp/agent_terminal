# this file contains function to build the agent graph and return it



from langgraph.graph import StateGraph, START, END
from Agent.utils.state import AgentState 
from Agent.utils.nodes import is_sys_ass_req, planner, retry, test_print_state



def get_graph():
    graph_builder = StateGraph(AgentState)
    graph_builder.add_node( "is_sys_ass_req", is_sys_ass_req )

    #test node
    graph_builder.add_node( "print_state", test_print_state )
    graph_builder.add_node( "planner", planner )
    graph_builder.add_node( "retry", retry )

    graph_builder.add_edge( START, "is_sys_ass_req" )
    graph_builder.add_edge( "is_sys_ass_req", "print_state" )
    graph_builder.add_edge( "print_state", END )

    return graph_builder.compile()
