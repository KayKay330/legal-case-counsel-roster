
import json
from argparse import ArgumentParser

from legal_case_app.presentation_layer.user_interface import UserInterface


def configure_and_parse_commandline_arguments():
    """Configure and parse command-line arguments."""
    parser = ArgumentParser(
        prog="main.py",
        description="Start the Legal Case Counsel Roster application.",
        epilog="POC: Your Name | your@email",
    )

    parser.add_argument(
        "-c",
        "--configfile",
        required=True,
        help="Path to JSON configuration file.",
    )

    args = parser.parse_args()
    return args


def main():
    """Application entry point."""
    # 1. Read command-line arguments
    args = configure_and_parse_commandline_arguments()

    # 2. Load the JSON config file
    with open(args.configfile, "r") as f:
        config = json.load(f)

    # 3. Create and start the user interface (which uses AppServices → DB)
    ui = UserInterface(config)
    ui.start()


if __name__ == "__main__":
    main()
