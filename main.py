#!/usr/bin/env python3
"""
Main entry point for the wizard game
"""

from blessed import Terminal
from game import Arena, Wizard, Crystal
from menu import Menu

def main():
    # Show menu
    menu = Menu()
    if not menu.display():
        print("Thanks for playing!")
        return

    # Initialize terminal
    term = Terminal()
    
    x,y=0,0

    # Create the game objects
    arena = Arena(size=10)
    wizard = Wizard(x, y, arena)
    crystal = Crystal(4, 4, arena)

    # Number buffer for #G command
    number_buffer = ""

    with term.cbreak(), term.hidden_cursor():
        loop = True
        while loop:
            # Clear the screen
            print('\033[2J\033[3J\033[H')

            # Show the arena
            print(arena)

            # Display instructions
            print(f"Press 'h/j/k/l' to move left/up/down/right")
            print(f"Press '0/$' to teleport leftmost/rightmost")
            print(f"Press '#G' to teleport to row # (e.g., 5G for row 5)")
            print(f"Press 'Q' to quit")
            if number_buffer:
                print(f"Number buffer: {number_buffer}")

            # Wait for input
            key = term.inkey()

            #Handle quit
            if key.lower() == 'q':
                loop = False

            # Movement vectors as tuples
            movements = {
                    'h': (-2, 0), # Left
                    'l': (2, 0), # Right
                    'k': (0, -1), #Up
                    'j': (0, 1) #Down
            }

            # Movement Handling
            if key.lower() in movements:
                dx, dy = movements[key.lower()]
                current_x, current_y = wizard.position
                new_x = current_x + dx
                new_y = current_y + dy
            
            # Check boundaries
                if ( 0 <= new_x <= (arena._size -1) * 2 and
                    0 <= new_y <= arena._size -1):
                    wizard.position = (new_x, new_y)
            
            elif key == '0': # Go to start of current row
                _, current_y = wizard.position
                wizard.position = (0, current_y)

            elif key == '$': # Go to end of current row
                _, current_y = wizard.position
                wizard.position = ((arena._size -1) * 2, current_y)
                number_buffer = "" # Clear buffer
            
            # collision detection
            if wizard.collision(crystal):
                # call the crystal re-render method
                # crystal.spawn() 
                pass

            # Handle number input (0-9)
            elif key.isdigit() and key != '0': # We have to skip 0 since 0 already snaps us back to first column...
                number_buffer += key

            # Handle G command for row teleportation
            elif key == 'G' and number_buffer:
                target_row = int(number_buffer)
                curent_x, _ = wizard.position

                # Check if target row is valid
                if 0 <= target_row <= arena._size -1:
                    wizard.position = (current_x, target_row)

                number_buffer = "" # Clearing buffer after use of G command

            # Clear buffer on other keys
            elif key and not key.isdigit():
                number_buffer = ""

    # Clear screen on exit
    print(term.clear)
    print("The wizard has left the building")

if __name__ == "__main__":
    main()
