import os
import random

import mech
import items
import inventory
import msg
import character_picking

import opening_screen
import how_to_play_screen

# decrements item count associated with item_hilite_coords_list from invt
def use_item_handler(invt, item_type, item_hilite_coords_list, selected_index):
    # item_hilite_coords_list might look like this:
    # [ ['Weapon', [['Axe', 5, 3, 21], ...] ]
    #   ['Armor', [['armor1', 13, 3, 21], ...] ]
    # ]
    # the numbers in sub-lists are: y and x begin of hilite, and length
    # invt = { "Weapon": {"Axe":1, "Knife":7, "w1":9, "w2":9, "w3":9}, ... }
    for i in range(len(item_hilite_coords_list)):
        if item_hilite_coords_list[i][0] == item_type:
            if selected_index in range(len(item_hilite_coords_list[i][1])):
                # access item name which will be our key to modifying invt
                item = item_hilite_coords_list[i][1][selected_index][0]
                invt[item_type][item] -= 1
                if invt[item_type][item] == 0:
                    del invt[item_type][item]
                    if not invt[item_type]:
                        del invt[item_type] # delete empty sub_inventory


def main ():
    #opening_screen.open_welcome_screen()
    #how_to_play_screen.how_to_play_screen()

    prot_name, prot_class = character_picking.pick_character()

    map = mech.load_map("map_level_1.txt")
    prot_pos = [ len(map[0]) - 4, 4 ] #[random.randint(map_xmin, map_xmax), random.randint(map_ymin, map_ymax)]
    steer_keys = ("w", "s", "a", "d")

    antagonists = ["¤", "O"]
    antag_hp = 10

    # load items that will be collectible from map
    items_collection = items.load_items()
    # locate antagonists and items (predefined symbols) in our map for further handling
    antags_coords = []
    items_coords = []
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == antagonists[0]: # count *only* singular cancer cells
                antags_coords.append([[x,y], antag_hp])
            if map[y][x] == "i":
                items_coords.append([ [x,y], random.randint(0, len(items_collection) - 1)] )


    protagonist = "@"
    # save the character at which protagonist will be placed; it will be restored after prot makes a move
    old_char = [map[prot_pos[1]][prot_pos[0]]]
    map[prot_pos[1]][prot_pos[0]] = protagonist

    # load primary inventory
    invt = { "Weapon": {"Axe":1, "Knife":7 },
                "Potion": {"pot1":3 },
                "Armor": {"armor1":5 }
            }
    invtable = [] # inventory nicely converted to ascii will sit here, it is loaded a little later

    prot_traits = { "Lives":10, "Experience":7,
                    "Attack":5, "Defense":5, "Agility":5, "Strength":10,
                    "Load capacity":777 }

    message_output = []

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
        invtable = inventory.generate_inventory_table(invt, item_hilite_coords_list, prot_traits)

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

        # print a horizontal bind of (inventory table) and (vertical bind of map and message output), highlighting appropriate entries in inventory table
        mech.print_map(mech.bind_maps_horz(invtable, mech.bind_maps_vert(map, message_output)), hilite_coords)
        if len(antags_coords) == 0:
            print("Defeated antags.")
            break

        # take a character from input
        user_input = mech.getch()
        # check input
        if user_input.lower() in steer_keys:
            still_in_play = mech.handle_protagonist_move(map, user_input, message_output, protagonist, prot_pos, prot_traits, antagonists, old_char, items_coords, items_collection, invt)
            if not still_in_play:
                break

        elif user_input == " ":
            #check antagonist proximity and apply damage if applicable
            mech.handle_player_attack(map, prot_pos, antags_coords)

        elif user_input == "i":
            weapon_selection_index += 1
        elif user_input == "o":
            armor_selection_index += 1
        elif user_input == "p":
            potion_selection_index += 1

        elif user_input == "j":
            use_item_handler(invt, "Weapon", item_hilite_coords_list, weapon_selection_index)
        elif user_input == "k":
            use_item_handler(invt, "Armor", item_hilite_coords_list, armor_selection_index)
        elif user_input == "l":
            use_item_handler(invt, "Potion", item_hilite_coords_list, potion_selection_index)

        elif user_input == "x":
            break



if __name__ == "__main__":
    main()
