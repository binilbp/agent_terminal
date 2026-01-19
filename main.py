import argparse

from config.settings import SETTINGS
from TUI.ui import app
from Agent.cli_agent import run_cli_agent 



if __name__ == "__main__":

    parser = argparse.ArgumentParser()


    #defining the args type
    parser.add_argument('--run', type=str, help='Specify a run type: cli/tui. Default tui. eg python main.py --run cli')

    args = parser.parse_args()

    if args.run == "cli":
        run_cli_agent()

    else:
        # normal mode run TUI
        app.run()
