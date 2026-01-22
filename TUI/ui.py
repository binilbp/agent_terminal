from textual.app import App, ComposeResult
from textual.widgets import TabbedContent, TabPane, Label, Footer, TextArea, Button, RichLog
from textual.containers import Container, Vertical, Horizontal
from textual import on, work
from rich.markdown import Markdown
from langchain_core.messages import HumanMessage
from Agent.graph import get_graph
from TUI.helper_functions import write_log


# Logo import
class ASCIName(Container):
    def compose(self) -> ComposeResult:
        try:
            with open("arts/linquix_ascii.txt", "r") as artfile:
                art = artfile.read()
        except FileNotFoundError:
            art = "LINQUIX"
        yield Label(art, id="ascii")

class Agent(Container):
    def compose(self) -> ComposeResult:
        agent_box = RichLog(
                id="agent-box",
                auto_scroll = True, 
                highlight=True, 
                markup = True
        )
        agent_box.border_title = "Terminal"
        yield agent_box

    def on_mount(self) -> None:
        self.query_one("#agent-box", RichLog).write("  [blue] [/]  How can I help you today?\n", animate = True)
        # write_log(self,icon="[blue] [/]", content = "How can i help you ?")
class Input(Horizontal):
    def compose(self) -> ComposeResult:
        input_box = TextArea(id="input-box")
        input_box.border_title = "Input"
        input_box.placeholder = "Type your query here.."
        input_box.highlight_cursor_line = False
        yield input_box
        with Vertical(id="input-buttons"):
            yield Button("", id="send-button")
            yield Button("", id="stop-button")

class Command(Horizontal):
    def compose(self) -> ComposeResult:
        command_box = TextArea(id="command-box")
        command_box.border_title = "Command"
        yield command_box
        with Vertical(id="command-buttons"):
            yield Button("", id="execute-button")
            yield Button("", id="stop-button")

class Terminal(Vertical):
    def compose(self) -> ComposeResult:
        yield Agent()
        with TabbedContent(id="input-command-tabbed"):
            with TabPane("Send Input", id="input-tab"):
                yield Input()
            with TabPane("Execute Command", id="command-tab"):
                yield Command()

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

    @on(Button.Pressed, "#send-button")
    def handle_send_button(self, event: Button.Pressed) -> None:
        input_box = self.query_one("#input-box", TextArea)
        user_input = input_box.text.strip()
        
        send_button = self.query_one("#send-button", Button)

        if user_input:
            # Clear the input box
            input_box.text = ""

            send_button.loading = True
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
                        send_button.loading = False
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
