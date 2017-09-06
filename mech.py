import os
import math


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
Loads a map from a file filename.
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

    return map


def print_map (map):
    for row in map:
        for char in row:
            print(char, end="")
        print()


'''
Returns true if a character would collide
with character `what` if moved at `char_coords` in map, false otherwise
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


def handle_protagonist_move(map, direction, protagonist, prot_pos, antagonist, old_char):
    dx = 0
    dy = 0
    if direction == "w":
        # up, decrement y
        dy = -1
    elif direction == "s":
        # down, increment y
        dy = 1
    elif direction == "a":
        # left, decrement x
        dx = -1
    elif direction == "d":
        # right, increment x
        dx = 1

    x_new = prot_pos[0] + dx
    y_new = prot_pos[1] + dy
    prot_pos_new = [x_new, y_new]

    would_step_at_wall = check_collision(map, prot_pos_new, "#")
    would_step_at_antag = check_collision(map, prot_pos_new, antagonist)

    if would_step_at_wall:
        # end of gameplay
        print("You've touched lava! You lost!")
        return False
    elif would_step_at_antag:
        pass # do nothing, don't step at the antagonist
    else:  # perform the move
        # restore previous character to old position
        map[prot_pos[1]][prot_pos[0]] = old_char[0]
        # save character to be stepped at for restoration
        old_char[0] = map[prot_pos_new[1]][prot_pos_new[0]]
        # move/ `draw` protagonist in new pos
        map[prot_pos_new[1]][prot_pos_new[0]] = protagonist
        # update char_pos to the outside world
        prot_pos[0] = x_new
        prot_pos[1] = y_new

    return True


def distance(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return int(math.floor(math.sqrt(dx*dx+dy*dy)))

def handle_player_attack(map, prot_pos, antags):
    #antags is a list of lists of form [[x,y], hp]
    #prot_pos is a [x,y]
    for i in range(len(antags)):
        if distance(prot_pos, antags[i][0]) <= 1:
            # decrement antag hp
            antags[i][1] -= 1
            if antags[i][1] <= 0:
                # antag dead, wipe from map
                antag_x = antags[i][0][0]
                antag_y = antags[i][0][1]
                map[antag_y][antag_x] = " "
                # mark as dead for deletion
                antags[i] = []

    # traverse antags list and delete dead ones
    while [] in antags:
        del antags[antags.index([])] # the while condition guarantees that there is at least one []
