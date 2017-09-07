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

def get_predefined_color(color):
    colors = {
        "black"     :"\033[30m",
        "red"       :"\033[31m",
        "green"     :"\033[32m",
        "orange"    :"\033[33m",
        "blue"      :"\033[34m",
        "purple"    :"\033[35m",
        "cyan"      :"\033[36m",
        "lightgrey" :"\033[37m",
        "darkgrey"  :"\033[90m",
        "lightred"  :"\033[91m",
        "lightgreen":"\033[92m",
        "yellow"    :"\033[93m",
        "lightblue" :"\033[94m",
        "pink":     "\033[95m",
        "lightcyan" :"\033[96m"
        }
    if color not in colors:
        raise KeyError("invalid color specifier")

    return colors[color]

# hilite coords is a list consisting of lists like:
# ['Axe', y, x, hilite length]
def print_map (map, hilite_coords):
    coord_dict = {}
    for i in range(len(hilite_coords)):
        # sieve out y: [x, length of hilite]
        coord_dict[hilite_coords[i][1]] = [hilite_coords[i][2], hilite_coords[i][3]]

    for y in range(len(map)):
        for x in range(len(map[y])):
            #                      x_start          <= x < x_start          + length of hilite
            if y in coord_dict and coord_dict[y][0] <= x < coord_dict[y][0] + coord_dict[y][1]:
                # print with inverted color: inventory selected item
                print("\033[7m" + map[y][x] + "\033[0m", end="")
            else:
                # print normally, optionally in colors
                color = "\033[0m" # default
                if map[y][x] == "<":
                    color = get_predefined_color("lightgreen")
                elif map[y][x] == "#":
                    color = get_predefined_color("red")
                elif map[y][x] == "~":
                    color = get_predefined_color("orange")

                print(color + map[y][x] + "\033[0m", end="")
        print()


def bind_maps(left, right):
    left_indent = [" "] * len(left[0])
    bound = []
    if len(right) > len(left):
        for i in range(len(right)):
            if i < len(left):
                bound.append(left[i] + right[i])
            else:
                bound.append(left_indent + right[i])
    else:
        for i in range(len(left)):
            if i < len(right):
                bound.append(left[i] + right[i])
            else:
                bound.append(left[i])

    return bound


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


# returns an item tuple from items_collection; it *has* to exist since protagonist
# has stepped at it
def get_item_from_collection(prot_pos, items_coords, items_collection):
# prot_pos_new is a [x,y]
# items_coords = [ [[item1_x, item1_y], index1], ... ]
# items_collection = ((type1, item1, {trait1 : delta1, ... traitn : deltan}),
#                     (type2, item2, {trait2 : delta2, ... traitn : deltan}))
    item = ()
    # locate our item in items_collection with help of an associated
    # coordinate-index pair in item_coords
    for possible_item in items_coords:
        if possible_item[0][0] == prot_pos[0] and \
            possible_item[0][1] == prot_pos[1]:
            # we've found item match: grab its index
            index = possible_item[1]
            # access the particular item
            item = items_collection[index]

    if not item: # we have stepped at an item, so it *must* exist
        raise ValueError("something effed up tremendously...")

    return item


# returns True if protagonist is able (=> prot_traits allow) to lift an item at which
# it has stepped, False otherwise
def able_to_lift_item(prot_pos, prot_traits, items_coords, items_collection):
# prot_pos_new is a [x,y], prot_traits is a dict with string:int pairs
# items_coords = [ [[item1_x, item1_y], index1], ... ]
# items_collection = ((type1, item1, {trait1 : delta1, ... traitn : deltan}),
#                     (type2, item2, {trait2 : delta2, ... traitn : deltan}))

    item = get_item_from_collection(prot_pos, items_coords, items_collection)

    #weapons and armor have weight 1 each, potions are weightless
    if item[0] == "Potion":
        return True
    elif item[0] == "Weapon" or item[0] == "Armor":
        if prot_traits["load_capacity"] < 1: #cannot take it?
            return False
        return True

    raise ValueError("unknown item type %s" % (item[0]))


def adjust_inventory_prot_traits(invt, prot_traits, item):
# invt is a { "Weapon": {"Axe":1, "Knife":7, "w1":9, "w2":9, "w3":9}, ... }
# prot_traits is a dict with string:int pairs
# item is a (type1, item1, {trait1 : delta1, ... traitn : deltan})

    # update protagonist traits
    trait_dict = item[2]
    for trait in trait_dict:
        if trait in prot_traits:
            prot_traits[trait] += trait_dict[trait]
        else:
            prot_traits[trait] = trait_dict[trait] # add trait if it wasn't present

    # update inventory
    item_type = item[0]
    item_name = item[1]
    # create item category/ type if absent
    if item_type not in invt:
        invt[item_type] = {}

    if item_name in invt[item_type]:
        # adjust item amount
        invt[item_type][item_name] += 1
    else:
        # add the item
        invt[item_type][item_name] = 1


def handle_protagonist_move(map, direction, protagonist, prot_pos, prot_traits, antagonists, old_char, items_coords, items_collection, invt):
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

    #check collisions
    # any antagonist?
    would_step_at_any_antag = False
    for antag in antagonists:
        if check_collision(map, prot_pos_new, antag):
            would_step_at_any_antag = True
            break

    # any item?
    would_step_at_item = check_collision(map, prot_pos_new, "i")

    # any deadly wall?
    cannot_step_at = "#~|"
    would_step_at_any_deadly = False
    for disallowed in cannot_step_at:
        if check_collision(map, prot_pos_new, disallowed):
            # about to step at one of disallowed characters?
            would_step_at_any_deadly = True
            break

    # examine collisions
    if would_step_at_any_deadly:
        # end of gameplay
        print("You've touched lava! You lost!")
        return False
    elif would_step_at_any_antag:
        pass # do nothing, antagonists cannot be stepped at
    elif would_step_at_item and not able_to_lift_item(prot_pos_new, prot_traits, items_coords, items_collection):
        pass
        # todo: print message about not being able to collect an item
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
        # have we stepped at an item (we are not overloaded)?
        if old_char[0] == "i":
            # protagonist has stepped at an item: its coordinates reflect one of those in items_coords
            # items_coords = [ [[item1_x, item1_y], index1], ... ]
            item = get_item_from_collection(prot_pos, items_coords, items_collection)
            # apply item to inventory and protagonist traits
            adjust_inventory_prot_traits(invt, prot_traits, item)
            old_char[0] = " " # will wipe item after we have moved somewhere else

    return True


def distance(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return int(math.floor(math.sqrt(dx*dx+dy*dy)))

def handle_player_attack(map, prot_pos, antags_coords):
    #antags_coords is a list of lists of form [[x,y], hp]
    #prot_pos is a [x,y]
    for i in range(len(antags_coords)):
        if distance(prot_pos, antags_coords[i][0]) <= 1:
            # decrement antag hp
            antags_coords[i][1] -= 1
            if antags_coords[i][1] <= 0:
                # antag dead, wipe from map
                antag_x = antags_coords[i][0][0]
                antag_y = antags_coords[i][0][1]
                map[antag_y][antag_x] = " "
                # mark as dead for deletion
                antags_coords[i] = []

    # traverse antags_coords list and delete dead ones
    while [] in antags_coords:
        del antags_coords[antags_coords.index([])] # the while condition guarantees that there is at least one []
