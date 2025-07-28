#!/usr/bin/env python3
"""
Menu system for VimWizards game
"""

from blessed import Terminal
from database import get_top_high_scores

class Menu:
    def __init__(self):
        self.term = Terminal()
        self.logo = self.load_logo("assets/ascii/logo.txt")
        self.options = ['Start Game', 'High Scores', 'Quit']
        self.selected = 0

    def load_logo(self,path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return "[Logo file not found]"

    def display_high_scores(self):
        """Display the high scores screen."""
        with self.term.cbreak(), self.term.hidden_cursor():
            while True:
                # Clear screen
                print('\033[2J\033[3J\033[H')
                
                # Display header
                print("HIGH SCORES")
                print("=" * 50)
                print()
                
                # Get top 10 scores
                scores = get_top_high_scores(10)
                
                if not scores:
                    print("No high scores yet!")
                    print("Be the first to set a record!")
                else:
                    print(f"{'Rank':<6} {'Initials':<10} {'Score':<10} {'Date'}")
                    print("-" * 50)
                    
                    for i, (initials, score, date) in enumerate(scores, 1):
                        # Format date to show just the date part (YYYY-MM-DD)
                        formatted_date = date.split()[0] if ' ' in date else date
                        print(f"{i:<6} {initials:<10} {score:<10} {formatted_date}")
                
                print()
                print("Press any key to return to main menu...")
                
                # Wait for any key press
                self.term.inkey()
                return

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
                    elif self.selected == 1:  # High Scores
                        self.display_high_scores()
                        # Continue the menu loop after returning from high scores
                    else:  # Quit
                        return False
