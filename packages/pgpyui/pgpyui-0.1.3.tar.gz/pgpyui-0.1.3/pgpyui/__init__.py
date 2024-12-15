"""

PygamePythonUI library (pgpyui) v.0.1.3

The MIT License Copyright © 2024 Memdved

"""

import pygame
from typing import Callable
import argparse
import webbrowser

def main():
    """Parses command-line arguments and displays help or opens documentation."""
    parser = argparse.ArgumentParser(description="PygamePythonUI library")
    parser.add_argument("--help", action="help", help="Show this help message and exit.")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.3")
    args = parser.parse_args()

    # Check if --help is provided, otherwise it's assumed the user wants docs
    if args.help:
        parser.print_help()
    else:
        doc_path = "docs/build/html/index.html"  # Path relative to the script
        try:
            webbrowser.open("file://" + doc_path)
        except FileNotFoundError:
            print(f"Error: Documentation file not found at {doc_path}")


if __name__ == "__main__":
    main()