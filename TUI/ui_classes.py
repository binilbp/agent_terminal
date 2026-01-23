#this file contains all the classes used for building the ui, these are called to ui.py file
from textual.app import ComposeResult
from textual.widgets import TabbedContent, TabPane, Label, Footer, TextArea, Button, RichLog, LoadingIndicator
from textual.containers import Container, Vertical, Horizontal



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



class StatusBar(Horizontal):
    def compose(self) -> ComposeResult:
        yield LoadingIndicator(id="loading-bar")
        status_line = RichLog(
                id="status-line",
                markup = True
        )
        yield status_line

    def on_mount(self) -> None:
        self.query_one("#status-line", RichLog).write("Type your query and press [green][/] to get started")
        


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
        yield StatusBar(id="status-bar")

        with TabbedContent(id="input-command-tabbed"):
            with TabPane("Send Input", id="input-tab"):
                yield Input()
            with TabPane("Execute Command", id="command-tab"):
                yield Command()



# the following functions goes to the settings tab of app
from config.settings import SETTINGS
from rich.json import JSON

class ViewSettings(Container):
    def compose(self) -> ComposeResult:
        settings_box = RichLog(id = "settings-box")
        yield settings_box

    def on_mount(self) -> None:
        # pretty_settings =  JSON.from_data(SETTINGS)
        self.query_one("#settings-box", RichLog).write(SETTINGS)



