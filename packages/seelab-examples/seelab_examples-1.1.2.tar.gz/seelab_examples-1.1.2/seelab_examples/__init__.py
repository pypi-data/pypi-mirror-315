# seelab_examples/__init__.py

import sys,os, json
from .layouts import QtVersion,utils  # Added import for QtVersion
from PyQt5 import QtWidgets
import argparse  # Added import for argparse

from .script_runner import ScriptRunner  # Adjust the import based on your actual script structure


def load_experiments(file_path):
    """Load experiments from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def main():
    """Main entry point for the app_examples module."""
    # Load experiments from experiments.json
    experiments_file = os.path.join(os.path.dirname(__file__), 'experiments.json')
    experiments = load_experiments(experiments_file)

    # Create a list of choices for the argument parser
    choices = []
    for category, items in experiments.items():
        for item in items:
            if item['module_name']:  # Ensure module_name is not empty
                choices.append((item['module_name'], item['title']))

    parser = argparse.ArgumentParser(description='Run a specific script from seelab_examples.')

    # Add a custom help message to show the table of names and titles
    parser.add_argument('--list', action='store_true', help='Show available experiments')

    # Now add the script argument after checking for --list
    parser.add_argument('script', nargs='?', choices=[name for name, title in choices], help='The name of the script to run')

    # Parse the arguments
    args = parser.parse_args()

    if args.list:
        print("Available Experiments:")
        print(f"{'Module Name':<30} {'Title'}")
        print("-" * 50)
        for name, title in choices:
            if title:
                print(f"{name:<30} {title}")
        sys.exit()


    os.chdir(os.path.dirname(__file__))
    app = QtWidgets.QApplication(sys.argv)
    window = ScriptRunner(args)
    window.show()
    sys.exit(app.exec_())

# No need for the if __name__ == "__main__": block here anymore
