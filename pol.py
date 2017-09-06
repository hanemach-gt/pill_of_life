import os

import mech
import items
import opening_screen
import how_to_play_screen


def main ():
    opening_screen
    how_to_play_screen

    map = mech.load_map()
    prot_pos = [ len(map[0]) - 4, 4 ] #[random.randint(map_xmin, map_xmax), random.randint(map_ymin, map_ymax)]
    steer_keys = ("w", "s", "a", "d")

    antagonist = "¤"
    antag_hp = 10
    # locate antagonists in our map for further handling
    antags = []
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == antagonist:
                antags.append([[x,y], antag_hp])


    protagonist = "@"
    # save the character at which protagonist will be placed; it will be restored after prot makes a move
    old_char = [map[prot_pos[1]][prot_pos[0]]]
    map[prot_pos[1]][prot_pos[0]] = protagonist
    # load items
    items_collection = items.load_items()
    print(items_collection)
    os.system("sleep 5")
    while True:
        # clear the terminal
        os.system("clear")
        # print map
        mech.print_map(map)
        if len(antags) == 0:
            print("Defeated antags.")
            break

        # take a character from input
        user_input = mech.getch()
        # check input
        if user_input.lower() in steer_keys:
            still_in_play = mech.handle_protagonist_move(map, user_input, protagonist, prot_pos, antagonist, old_char)
            if not still_in_play:
                break

        elif user_input == " ":
            #check antagonist proximity and apply damage if applicable
            mech.handle_player_attack(map, prot_pos, antags)

        elif user_input == "x":
            break



if __name__ == "__main__":
    main()
