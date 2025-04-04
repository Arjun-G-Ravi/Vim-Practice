'''
Will develop after a while, have to use this as a foundation to write a proper version

'''
import curses
import random

def main(stdscr):
    # Initialize curses
    curses.curs_set(0) 
    stdscr.timeout(700)  # Refresh rate
    
    # Get screen dimensions
    sh, sw = stdscr.getmaxyx()
    
    # Initial player position (center of screen)
    player_y = sh // 2
    player_x = sw // 2
    
    # Generate initial set of targets
    num_targets = 3
    targets = []
    for _ in range(num_targets):
        targets.append([
            random.randint(0, sh-1),
            random.randint(0, sw-1)
        ])
    
    def draw_menu():
        stdscr.clear()
        options = [
            "1. Practice hjkl motions",
            "2. Coming soon...",
            "3. Coming soon..."
        ]
        for i, option in enumerate(options):
            stdscr.addstr(sh//2 - 1 + i, sw//2 - len(option)//2, option)
        stdscr.refresh()
        
        while True:
            key = stdscr.getch()
            if key == ord('1'):
                return True
            elif key == ord('q'):
                return False
    
    def game_loop():
        nonlocal player_y, player_x, targets
        
        # Variable to store numeric prefix
        count_buffer = ""
        
        while True:
            # Clear screen
            stdscr.clear()
            
            # Draw targets
            for target_y, target_x in targets:
                if 0 <= target_y < sh and 0 <= target_x < sw:
                    stdscr.addch(target_y, target_x, '@')
            
            # Draw player
            if 0 <= player_y < sh and 0 <= player_x < sw:
                stdscr.addch(player_y, player_x, 'X')
            
            # Show current count buffer in top left corner
            stdscr.addstr(0, 0, f"Count: {count_buffer}")
            
            # Refresh screen
            stdscr.refresh()
            
            # Handle input
            key = stdscr.getch()
            
            # Handle numeric prefix
            if ord('0') <= key <= ord('9'):
                count_buffer += chr(key)
                continue
            
            # Get count value (default to 1 if no number specified)
            count = int(count_buffer) if count_buffer else 1
            count_buffer = ""  # Reset buffer after motion
            
            # Vim motions with count support
            if key == ord('h') and player_x > 0:          # left
                player_x = max(player_x - count, 0)
            elif key == ord('j') and player_y < sh-1:     # down
                player_y = min(player_y + count, sh-1)
            elif key == ord('k') and player_y > 0:        # up
                player_y = max(player_y - count, 0)
            elif key == ord('l') and player_x < sw-1:     # right
                player_x = min(player_x + count, sw-1)
            elif key == ord('0') and player_x > 0:        # beginning of line
                player_x = 0  # Count doesn't make sense here
            elif key == ord('$') and player_x < sw-1:     # end of line
                player_x = sw-1  # Count doesn't make sense here
            elif key == ord('g'):                         # gg - top of screen
                next_key = stdscr.getch()
                if next_key == ord('g') and player_y > 0:
                    player_y = 0  # Count doesn't make sense here
            elif key == ord('G') and player_y < sh-1:     # bottom of screen
                player_y = sh-1  # Count doesn't make sense here
            elif key == ord('w') and player_x < sw-1:     # forward to start of next word
                player_x = min(player_x + (5 * count), sw-1)
            elif key == ord('b') and player_x > 0:        # backward to start of word
                player_x = max(player_x - (5 * count), 0)
            elif key == ord('e') and player_x < sw-1:     # forward to end of word
                player_x = min(player_x + (4 * count), sw-1)
            elif key == ord('{') and player_y > 0:        # up a paragraph
                player_y = max(player_y - (5 * count), 0)
            elif key == ord('}') and player_y < sh-1:     # down a paragraph
                player_y = min(player_y + (5 * count), sh-1)
            elif key == ord('q'):                         # quit
                break
            
            # Check if player is on a target
            player_pos = [player_y, player_x]
            if player_pos in targets:
                targets.remove(player_pos)
                # Add new target
                while True:
                    new_target = [
                        random.randint(0, sh-1),
                        random.randint(0, sw-1)
                    ]
                    if new_target != player_pos and new_target not in targets:
                        targets.append(new_target)
                        break
    
    # Show menu and start game if selected
    if draw_menu():
        game_loop()

# Run the game
curses.wrapper(main)