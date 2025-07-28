#!/usr/bin/env python3
"""
Game Over screen module for VimWizards.
Handles the game over display, initials input, and score saving using blessed terminal.
"""

from datetime import datetime
from blessed import Terminal
from database import save_high_score


class GameOverScreen:
    """Handles the game over screen display and user input."""
    
    def __init__(self):
        """Initialize the game over screen with terminal."""
        self.term = Terminal()
    
    def load_ascii_art(self):
        """Load the ASCII art from file."""
        try:
            with open("assets/ascii/game_over.txt", 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return "GAME OVER"
        except Exception:
            return "GAME OVER"
    
    def clear_screen(self):
        """Clear the terminal screen using ANSI escape sequences."""
        print('\033[2J\033[3J\033[H', end='', flush=True)
    
    def display_game_over(self, score, message=""):
        """Display the game over screen with ASCII art and score."""
        self.clear_screen()
        
        # Show ASCII art
        ascii_art = self.load_ascii_art()
        print(ascii_art)
        
        # Show score
        print(f"Final Score: {score}")
        print()
        
        # Show additional message if provided
        if message:
            print(message)
            print()
    
    def get_player_initials(self):
        """
        Get 3-character initials from the player using blessed terminal.
        Allows character-by-character input with Enter to submit when 3 characters.
        """
        initials = ""
        
        while True:
            self.display_game_over(0, "Enter your initials (3 characters):")
            print(f"Initials: {initials}_")
            print()
            print("Enter 3 letters for your initials")
            if len(initials) == 3:
                print("Press Enter to submit or Backspace to edit")
            
            with self.term.cbreak():
                key = self.term.inkey()
                
                if key.name == 'KEY_ESCAPE':
                    # User pressed Escape, cancel entry
                    return ""
                elif key.name == 'KEY_BACKSPACE' or key == '\x7f':
                    # Backspace - remove last character
                    if initials:
                        initials = initials[:-1]
                elif key.name == 'KEY_ENTER' or key == '\r' or key == '\n':
                    # Enter - submit if we have 3 characters
                    if len(initials) == 3:
                        return initials.upper()
                    # Otherwise ignore Enter if not 3 characters
                elif key.isalpha() and len(initials) < 3:
                    # Add letter if we don't have 3 yet
                    initials += key.upper()
                    
                    # Auto-submit when we reach 3 characters and user presses Enter
                    if len(initials) == 3:
                        # Show the completed initials
                        self.display_game_over(0, "Enter your initials (3 characters):")
                        print(f"Initials: {initials}")
                        print()
                        print("Press Enter to submit or Backspace to edit")
                        
                        # Wait for Enter or continue editing
                        with self.term.cbreak():
                            next_key = self.term.inkey()
                            if next_key.name == 'KEY_ENTER' or next_key == '\r' or next_key == '\n':
                                return initials.upper()
                            elif next_key.name == 'KEY_BACKSPACE' or next_key == '\x7f':
                                initials = initials[:-1]
                            elif next_key.name == 'KEY_ESCAPE':
                                return ""
    
    def save_score(self, initials, score):
        """Save the score to the database."""
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return save_high_score(initials, score, current_date)
    
    def wait_for_continue(self, message="Press any key to continue..."):
        """Wait for user to press any key."""
        print(message)
        with self.term.cbreak():
            self.term.inkey()
    
    def show(self, score):
        """
        Display the game over screen and handle score entry.
        
        Args:
            score: The player's final score
        """
        # Show initial game over screen
        self.display_game_over(score)
        self.wait_for_continue()
        
        # Get player initials
        initials = self.get_player_initials()
        
        # If user cancelled, don't save score
        if not initials:
            self.display_game_over(score, "Score not saved.")
            self.wait_for_continue()
            return
        
        # Save score to database
        save_success = self.save_score(initials, score)
        
        # Show confirmation
        if save_success:
            message = f"Score saved successfully for {initials}!"
        else:
            message = "Error saving score to database."
        
        self.display_game_over(score, message)
        self.wait_for_continue()


def test_game_over():
    """Test the game over functionality."""
    print("Testing Game Over screen...")
    game_over = GameOverScreen()
    game_over.show_game_over(42)
    print("Game Over test completed.")


if __name__ == "__main__":
    test_game_over()
