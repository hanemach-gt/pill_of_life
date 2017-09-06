import os

import mech
import items
import inventory

import opening_screen
import how_to_play_screen


def main ():
    #opening_screen.open_welcome_screen()
    #how_to_play_screen.how_to_play_screen()

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

    # load items that will be collectible from map
    items_collection = items.load_items()

    # load primary inventory
    invt = { "Weapon": {"Axe":1, "Knife":7, "w1":9, "w2":9, "w3":9},
                "Potion": {"pot1":3, "pot2":4, "pot3":4, "pot4":4, "pot5":4},
                "Armor": {"armor1":5, "armor2":9, "armor3":5, "armor4":9, "armor5":9 }
            }
    invtable = []

    weapon_selection_index = 0
    armor_selection_index = 0
    potion_selection_index = 0

    while True:
        # clear the terminal
        os.system("clear")
        # update inventory table map
        item_hilite_coords_list = []
        # the above list might look like this:
        # [ ['Weapon', [['Axe', 5, 3, 21], ... ]
        #   ['Armor', [['armor1', 13, 3, 21], ...]
        # ]
        # the numbers in sub-lists are: y and x begin of hilite, and length
        invtable = inventory.generate_inventory_table(invt, item_hilite_coords_list)
        # select from item_hilite_coords_list the coordinates that are of interest to us
        hilite_coords = []
        for sublist in item_hilite_coords_list:
            if "Weapon" in sublist:
                if weapon_selection_index not in range(len(sublist[1])): # check if we haven't retained an index of exhausted item
                    weapon_selection_index = 0
                hilite_coords.append(sublist[1][weapon_selection_index])

            if "Armor" in sublist:
                if armor_selection_index not in range(len(sublist[1])):
                    armor_selection_index = 0
                hilite_coords.append(sublist[1][armor_selection_index])

            if "Potion" in sublist:
                if potion_selection_index not in range(len(sublist[1])):
                    potion_selection_index = 0
                hilite_coords.append(sublist[1][potion_selection_index])

        # print a bind of maps, highlighting appropriate entries in inventory table
        mech.print_map(mech.bind_maps(invtable, map), hilite_coords)
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
        elif user_input == "i":
            weapon_selection_index +=1
        elif user_input == "o":
            armor_selection_index +=1
        elif user_input == "p":
            potion_selection_index +=1
        
        elif user_input == "x":
            break



if __name__ == "__main__":
    main()
