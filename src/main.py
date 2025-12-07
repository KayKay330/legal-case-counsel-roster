
"""
Main entry point for the Legal Case Counsel Roster Application.
"""

import json
from argparse import ArgumentParser

from legal_case_app.presentation_layer.user_interface import UserInterface


def configure_and_parse_commandline_arguments():
    """
    Configure and parse command-line arguments.
    This follows the book and professor's framework.
    """
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

    return parser.parse_args()


def main():
    """Application entry point."""

    # ---- 1. Read command-line arguments ----
    args = configure_and_parse_commandline_arguments()

    # ---- 2. Load JSON config ----
    with open(args.configfile, "r") as file:
        config = json.load(file)

    # ---- 3. Initialize User Interface ----
    ui = UserInterface(config)

    # ---- 4. TEST DATABASE CONNECTION (Chapter 24 Step 5) ----
    print("\nTesting MySQL connection...")
    try:
        results = ui.DB.db.test_connection()
        print("Connection successful! Sample rows:")
        print(results)
    except Exception as e:
        print("Connection failed:", e)
        raise

    # ---- 5. START APPLICATION ----
    ui.start()


if __name__ == "__main__":
    main()