# this file contains the most high level code for rendering the TUI, along with calling the graph for each user input


from textual.app import App, ComposeResult
from textual.widgets import TabbedContent, TabPane, Button, Label, Footer, TextArea, RichLog, LoadingIndicator
from textual.containers import Container, Vertical, Horizontal
from textual import on, work
from rich.markdown import Markdown
from langchain_core.messages import HumanMessage
from Agent.graph import get_graph
from TUI.helper_functions import write_log
from TUI.ui_classes import ASCIName, Terminal 



class App(App):
    
    CSS_PATH = "ui.tcss"
    theme = "dracula"

    
    def on_mount(self) -> None:
        """Initialize graph and session ID when app starts."""
        self.graph = get_graph()
        # Thread ID enables history persistence for clarification loops
        self.config = {"configurable": {"thread_id": "session_1"}}

        # variable to track running state
        self.is_agent_running = False
        #hide the loading-bar in the beggining
        self.query_one("#loading-bar").styles.display = "none"


    def compose(self) -> ComposeResult:
        with Vertical():
            yield ASCIName()
            with TabbedContent(id="main-tabbed"):
                with TabPane("Agent Terminal", id="terminal"):
                    yield Terminal()
                with TabPane("Settings", id="settings"):
                    yield Label("Settings Page")
            yield Footer()

    @on(Button.Pressed, "#stop-button")
    @on(Button.Pressed, "#stop-input-button")
    def handle_stop_button(self, event: Button.Pressed) -> None:
        if self.is_agent_running == True:
            self.is_agent_running = False
            # give notification to the user
            self.notify("Stopping generation..", severity="warning", timeout = 2.0)
            
            # send_button maybe disabled as we can stop before ai message retrieval,therefor enable send_button
            send_button = self.query_one("#send-button", Button)
            send_button.disabled = False
            # we should also hide the loading-bar
            self.query_one("#loading-bar").styles.display = "none"

    @on(Button.Pressed, "#send-button")
    def handle_send_button(self, event: Button.Pressed) -> None:
        input_box = self.query_one("#input-box", TextArea)
        user_input = input_box.text.strip()
        

        send_button = self.query_one("#send-button", Button)

        if user_input:
            # Clear the input box
            input_box.text = ""

            #disable the send_button util we get an ai reply, while enabling the loading-bar
            send_button.disabled = True
            self.query_one("#loading-bar").styles.display = "block"

            #change the is_running to true
            self.is_agent_running = True

            # Run the agent in a background thread
            self.run_agent_worker(user_input)

    @work(exclusive=True, thread=True)
    def run_agent_worker(self, user_input: str) -> None:
        """Execute Agent Logic in background to prevent freezing UI."""
        # CHANGED: Querying for RichLog
        agent_box = self.query_one("#agent-box", RichLog)
        
        # Display User Input
        write_log(self,icon="  [green] [/] ", content = f"{user_input}")

        # Prepare input for the graph
        inputs = {"messages": [HumanMessage(content=user_input)]}


        send_button = self.query_one("#send-button", Button)

        try:
            # Stream events from the graph
            events = self.graph.stream(inputs, config=self.config, stream_mode="values")

            for event in events:
                #check if running status is true
                if not self.is_agent_running:
                    write_log(self,icon="  [red] [/] ", content = "Process stopped by user\n")
                    break

                if "current_plan" in event:
                    current_plan = event["current_plan"]

                if "messages" in event:
                    last_message = event["messages"][-1]
                    
                    # Skip re-printing the user's own message
                    if isinstance(last_message, HumanMessage) and last_message.content == user_input:
                        continue

                    content = last_message.content

                    if last_message.type == "ai":
                        #enable the send_button again, since we got the ai message back
                        send_button.disabled = False
                        self.query_one("#loading-bar").styles.display = "none"

                        # Check for tool calls (internal thought process) vs final response
                        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                            tool_name = last_message.tool_calls[0]['name']
                            write_log(self,icon="  [red] [/] ", content = f"{tool_name} Tool Called")
                        else:
                            # Render with Markdown
                            write_log(self,icon="  [blue] [/] ", content = f"{content}")

                    elif last_message.type == "tool":
                         self.call_from_thread(lambda: agent_box.write(f"[TOOL OUTPUT]: {content}"))
        
        except Exception as e:
            self.call_from_thread(lambda: agent_box.write(f"\n[ERROR]: {str(e)}\n"))

        finally:
            self.is_agent_running = False


app = App()
