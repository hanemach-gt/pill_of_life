import random
import os

def getch():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

'''
Loads a map from a file. A map does not have to be a rectangle.
'''
def load_map (filename="map.txt"):
    map = []
    try:
        with open(filename) as file:
            for line in file:
                row = []
                for char in line.strip():
                    row.append(char)
                map.append(row)

    except FileNotFoundError:
        pass

    # `transpose` the list to be able to access [x][y] instead of [y][x]
    # find the longest row to complement
    return map


def print_map (map):
    for row in map:
        for char in row:
            print(char, end="")
        print()

'''
Checks if `char` would collide with `what` if moved on `char_coords` in map.
'''
def check_collision (map, char_coords, what):
    # coordinates to be tested against
    x_test = char_coords[0]
    y_test = char_coords[1]
    # bounds checking
    if not 0 <= x_test < len(map[0]) or \
        not 0 <= y_test < len(map):
        raise ValueError("at least one board list index out of bounds")

    if map[y_test][x_test] == what:
        return True

    return False


def handle_steer_keys(map, direction, char_pos):
    x_new = char_pos[0]
    y_new = char_pos[1]
    if direction == "w":
        # up, decrement y
        y_new -= 1
    elif direction == "s":
        # down, increment y
        y_new += 1
    elif direction == "a":
        # left, decrement x
        x_new -= 1
    elif direction == "d":
        # right, increment x
        x_new += 1

    char_pos_new = [x_new, y_new]

    will_collide_with_wall = check_collision(map, char_pos_new, "#")
    if will_collide_with_wall:
        # end of gameplay
        print("You've touched lava! You lost!")
        return False
    else:  # perform the move
        # wipe character from old position
        map[char_pos[1]][char_pos[0]] = " "
        # `draw` in new pos
        map[char_pos_new[1]][char_pos_new[0]] = "O"
        # update char_pos to the outside world
        char_pos[0] = x_new
        char_pos[1] = y_new

    #print_map(map)
    #os.system("read -p \"from handle steer keys\"")
    return True

def main ():
    map = load_map()
    dist_from_wall = 2
    map_xmin = dist_from_wall
    map_ymin = dist_from_wall
    map_xmax = len(map[0]) - dist_from_wall
    map_ymax = len(map) - dist_from_wall
    char_pos = [ len(map[0]) - 4, 4 ] #[random.randint(map_xmin, map_xmax), random.randint(map_ymin, map_ymax)]
    steer_keys = ("w", "s", "a", "d")
    # place our character randomly in a rectangle determined above by min-max points
    map[char_pos[1]][char_pos[0]] = "O"
    while True:
        # clear the terminal
        #os.system("sleep 0.5")
        os.system("clear")
        # print map
        print_map(map)
        # take a character from input
        user_input = getch()
        # check input
        if user_input.lower() in steer_keys:
            still_in_play = handle_steer_keys(map, user_input, char_pos)
            #print_map(map)
            #os.system("read -p \"in main after handle_steer_keys\"")
            if not still_in_play:
                break
        elif user_input == "x":
            break


main()
