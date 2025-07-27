#!/usr/bin/env python3
"""
Menu system for VimWizards game
"""

from blessed import Terminal

class Menu:
    def __init__(self):
        self.term = Terminal()
        self.logo = self.load_logo("assets/ascii/logo.txt")
        self.options = ['Start Game', 'Quit']
        self.selected = 0

    def load_logo(self,path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return "[Logo file not found]"

    def display(self):
        # Display the menu and handle user input
        with self.term.cbreak(), self.term.hidden_cursor():
            while True:
                # Clear screen
                print('\033[2J\033[3J\033[H')

                # Display logo
                print(self.logo)
                print()

                # Display menu options
                for i, option in enumerate(self.options):
                    if i == self.selected:
                        print(f"> {option}")
                    else:
                        print(f"  {option}")

                print()
                print("Use j/k to navigate, Enter to select")

                # Get user input
                key = self.term.inkey()

                if key.lower() == 'j' and self.selected < len(self.options) - 1:
                    self.selected += 1
                elif key.lower() == 'k' and self.selected > 0:
                    self.selected -= 1
                elif key.name == 'KEY_ENTER':
                    if self.selected == 0:  # Start Game
                        return True
                    else:  # Quit
                        return False
