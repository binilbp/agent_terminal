from textual.app import App, ComposeResult
from textual.widgets import TabbedContent, TabPane, Label, Footer, TextArea, Button
from textual.containers import Container, Vertical, Horizontal



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
        agent_box = TextArea(id="agent-box", read_only=True)
        agent_box.border_title = "Agent"
        agent_box.language = "markdown"
        agent_box.text = """How can I help you"""
        agent_box.show_cursor = False
        agent_box.highlight_cursor_line = False
        yield agent_box

class Input(Container):
    def compose(self) -> ComposeResult:
        input_box = TextArea(id="input-box")
        input_box.border_title = "Input"
        input_box.placeholder = "Type your query here.."
        yield input_box

class Command(Container):
    def compose(self) -> ComposeResult:
        command_box = TextArea(id="command-box")
        command_box.border_title = "Command"
        yield command_box



class Terminal(Vertical):
    def compose(self) -> ComposeResult:
        yield Agent()
        with TabbedContent(id="input-command-tabbed"):
            with TabPane("Input", id="input-tab"):
                yield Input()
            with TabPane("Command", id="command-tab"):
                yield Command()

class App(App):
    
    CSS_PATH = "ui.tcss"
    theme = "dracula"

    # BINDINGS = [
    #     Binding("^q", "quit", "quit", show=True),
    #     Binding("^k", "switch_mode('command')", "command", show=True),
    #     Binding("^u", "switch_mode('userinput')", "userinput", show=True),
    # ]

    def compose(self) -> ComposeResult:
        with Vertical():
            yield ASCIName()
            with TabbedContent(id="main-tabbed"):
                with TabPane("Agent Terminal", id="terminal"):
                    yield Terminal()
                with TabPane("Settings", id="settings"):
                    yield Label("Settings Page")
                
            yield Footer()



app = App()
