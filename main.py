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
    # Command mode buffer
    command_buffer = ""
    command_mode = False

    with term.cbreak(), term.hidden_cursor():
        loop = True
        while loop:
            # Clear the screen
            print('\033[2J\033[3J\033[H')

            # Show Crystals collected as score
            print(f"Score: {wizard.crystals}")

            # Show the arena
            print(arena)

            # Display instructions
            print(f"Press 'h/j/k/l' to move left/down/up/right")
            print(f"Press '0/$' to teleport leftmost/rightmost")
            print(f"Press '#G' to teleport to row # (e.g., 5G for row 5)")
            print(f"Press ':q!' to quit")
            if number_buffer:
                print(f"Number buffer: {number_buffer}")
            if command_mode:
                print(f":{command_buffer}")

            # Wait for input
            key = term.inkey()

            # Handle command mode
            if key == ':' and not command_mode:
                command_mode = True
                command_buffer = ""
            elif command_mode:
                if key.code == term.KEY_ENTER or key == '\r' or key == '\n':
                    # Execute command
                    if command_buffer == "q!":
                        loop = False
                    # Clear command mode
                    command_mode = False
                    command_buffer = ""
                elif key.code == term.KEY_ESCAPE or key == '\x1b':
                    # Exit command mode
                    command_mode = False
                    command_buffer = ""
                elif key.code == term.KEY_BACKSPACE or key == '\x7f' or key == '\b':
                    # Handle backspace
                    if command_buffer:
                        command_buffer = command_buffer[:-1]
                elif key and not key.is_sequence:
                    # Add character to command buffer
                    command_buffer += str(key)

            # Skip all game controls if in command mode
            elif not command_mode:
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
                        # Check if trying to move into the immediate tail segment
                        if wizard._tail and (new_x, new_y) == wizard._tail[0]:
                            pass  # Don't allow this move
                        else:
                            wizard.position = (new_x, new_y)
                            
                            # Check for tail collision
                            if wizard.collision_with_tail():
                                loop = False
            
                elif key == '0' and not number_buffer: # Go to start of current row only if buffer is empty
                    if not wizard.has_active_portal():
                        old_pos = wizard.position
                        _, current_y = wizard.position
                        new_pos = (0, current_y)
                        
                        # Only teleport if not moving to same position
                        if old_pos != new_pos:
                            wizard.create_portal(old_pos, new_pos)
                            wizard.position = new_pos
                            
                            # Check for tail collision
                            if wizard.collision_with_tail():
                                loop = False

                elif key == '$': # Go to end of current row
                    if not wizard.has_active_portal():
                        old_pos = wizard.position
                        _, current_y = wizard.position
                        new_pos = ((arena._size -1) * 2, current_y)
                        number_buffer = "" # Clear buffer
                        
                        # Only teleport if not moving to same position
                        if old_pos != new_pos:
                            wizard.create_portal(old_pos, new_pos)
                            wizard.position = new_pos
                            
                            # Check for tail collision
                            if wizard.collision_with_tail():
                                loop = False
            
                # collision detection
                if wizard.collision(crystal):
                    # call the crystal re-render method
                    wizard.collect_crystals()
                    crystal.spawn(wizard)

                # Handle number input (0-9)
                elif key.isdigit() and (key != '0' or number_buffer): # Allow 0 if buffer has content
                    number_buffer += key

                # Handle G command for row teleportation
                elif key == 'G' and number_buffer:
                    if not wizard.has_active_portal():
                        target_row = int(number_buffer) - 1 # Adjusted for zero index
                        old_pos = wizard.position
                        current_x, _ = wizard.position
                        new_pos = (current_x, target_row)

                        # Check if target row is valid and not same position
                        if 0 <= target_row <= arena._size -1 and old_pos != new_pos:
                            wizard.create_portal(old_pos, new_pos)
                            wizard.position = new_pos
                            
                            # Check for tail collision
                            if wizard.collision_with_tail():
                                loop = False

                    number_buffer = "" # Clearing buffer after use of G command

                # Clear buffer on other keys
                elif key and not key.isdigit():
                    number_buffer = ""
            
            # Check if portal should close (after all movements)
            wizard.check_portal_clear()

    # Clear screen on exit
    print(term.clear)
    
    # Game over screen
    if wizard.collision_with_tail():
        print("\n" * 5)
        print("=" * 40)
        print("         GAME OVER!")
        print("=" * 40)
        print(f"\nThe wizard collided with their tail!")
        print(f"Final Score: {wizard.crystals}")
        print("\nPress any key to exit...")
        
        # Wait for a key press before exiting
        with term.cbreak():
            term.inkey()
    else:
        print("The wizard has left the building")

if __name__ == "__main__":
    main()
