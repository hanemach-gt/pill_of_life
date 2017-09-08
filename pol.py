import os
import random

import mech
import items
import inventory
import msg
import character_picking
import hotwarm

import opening_screen
import how_to_play_screen


def extract_item_name(item_hilite_coords_list, item_type, index):
    # item_hilite_coords_list might look like this:
    # [ ['Weapon', [['Axe', 5, 3, 21], ...] ]
    #   ['Armor', [['armor1', 13, 3, 21], ...] ]
    # ]
    item_name = ""
    for i in range(len(item_hilite_coords_list)):
        if item_hilite_coords_list[i][0] == item_type:
            if index in range(len(item_hilite_coords_list[i][1])):
                item_name = item_hilite_coords_list[i][1][index][0]

    return item_name


# decrements item count associated with item_hilite_coords_list from invt
def use_item_handler(invt, item_type, item_hilite_coords_list, selected_index, prot_traits):
    # item_hilite_coords_list might look like this:
    # [ ['Weapon', [['Axe', 5, 3, 21], ...] ]
    #   ['Armor', [['armor1', 13, 3, 21], ...] ]
    # ]
    # the numbers in sub-lists are: y and x begin of hilite, and length
    # invt = { "Weapon": {"Axe":1, "Knife":7, "w1":9, "w2":9, "w3":9}, ... }
    # access item name which will be our key to modifying invt
    item = extract_item_name(item_hilite_coords_list, item_type, selected_index)
    if item:
        invt[item_type][item] -= 1
        if not item_type == "Potion":
            if "Load capacity" in prot_traits:
                prot_traits["Load capacity"] += 1
            else:
                prot_traits["Load capacity"] = 1

        if invt[item_type][item] == 0:
            del invt[item_type][item]
            if not invt[item_type]:
                del invt[item_type] # delete empty sub_inventory

# prints out selected item traits to player message output
def item_selection_msg_handler(item_hilite_coords_list, item_type, index, items_collection, message_output):
    # item_hilite_coords_list might look like this:
    # [ ['Weapon', [['Axe', 5, 3, 21], ...] ]
    #   ['Armor', [['armor1', 13, 3, 21], ...] ]
    # ]
    # items_collection = ((type1, item1, {trait1 : delta1, ... traitn : deltan}),
    #                     (type2, item2, {trait2 : delta2, ... traitn : deltan}))
    item_name = extract_item_name(item_hilite_coords_list, item_type, index)
    trait_dict = {}
    if item_name:
        for item in items_collection:
            if item[0] == item_type and item[1] == item_name:
                trait_dict = item[2]
                break

    traits_string = ""
    for trait in trait_dict:
        plus = ""
        if trait_dict[trait] > 0:
            plus = "+"
        traits_string += trait + " " + plus + str(trait_dict[trait]) + ",  "
    traits_string = traits_string.rstrip(",  ")

    result_msg = "Selected %s (%s), modifies %s, weighs %s" % (item_name, item_type, traits_string, "1" if not item_type=="Potion" else "nothing")
    msg.set_output_message(message_output, result_msg)


# returns True if level passed, False if lost, None
def engage_level(invt, prot_traits, items_collection, file_name, prot_initial_coords):
    map = mech.load_map(file_name)
    prot_pos = [ prot_initial_coords[0], prot_initial_coords[1] ] #[random.randint(map_xmin, map_xmax), random.randint(map_ymin, map_ymax)]
    steer_keys = ("w", "s", "a", "d")

    antagonists = ["¤", "O"]
    antag_hp = 10

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

    invtable = [] # inventory nicely converted to ascii will sit here, it is loaded a little later

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
                if armor_selection_index not in range(len(sublist[1])): # check if we haven't retained an index of exhausted item
                    armor_selection_index = 0
                hilite_coords.append(sublist[1][armor_selection_index])

            if "Potion" in sublist:
                if potion_selection_index not in range(len(sublist[1])): # check if we haven't retained an index of exhausted item
                    potion_selection_index = 0
                hilite_coords.append(sublist[1][potion_selection_index])

        # print a horizontal bind of (inventory table) and (vertical bind of map and message output), highlighting appropriate entries in inventory table
        mech.print_map(mech.bind_maps_horz(invtable, mech.bind_maps_vert(map, message_output)), hilite_coords)

        if prot_traits["Lives"] <= 0:
            return False

        if len(antags_coords) == 0:
            return True

        # take a character from input
        user_input = mech.getch()
        # check input
        if user_input.lower() in steer_keys:
            still_in_play = mech.handle_protagonist_move(map, user_input, message_output, protagonist, prot_pos, prot_traits, antagonists, old_char, items_coords, items_collection, invt)
            if not still_in_play:
                return False

        elif user_input == " ":
            #check antagonist proximity and apply damage if applicable
            # access currently selected Weapon
            weapon_name = extract_item_name(item_hilite_coords_list, "Weapon", weapon_selection_index)
            # item_hilite_coords_list might look like this:
            # [ ['Weapon', [['Axe', 5, 3, 21], ...] ]
            #   ['Armor', [['armor1', 13, 3, 21], ...] ]
            # ]
            # the numbers in sub-lists are: y and x begin of hilite, and length
            # invt = { "Weapon": {"Axe":1, "Knife":7, "w1":9, "w2":9, "w3":9}, ... }
            mech.handle_player_attack(map, prot_pos, antags_coords, prot_traits, message_output, invt, weapon_name)

        elif user_input == "i":
            weapon_selection_index += 1
            for sublist in item_hilite_coords_list:
                if "Weapon" in sublist:
                    if weapon_selection_index not in range(len(sublist[1])): # check if we haven't retained an index of exhausted item
                        weapon_selection_index = 0
            item_selection_msg_handler(item_hilite_coords_list, "Weapon", weapon_selection_index, items_collection, message_output)

        elif user_input == "o":
            armor_selection_index += 1
            for sublist in item_hilite_coords_list:
                if "Armor" in sublist:
                    if armor_selection_index not in range(len(sublist[1])):
                        armor_selection_index = 0
            item_selection_msg_handler(item_hilite_coords_list, "Armor", armor_selection_index, items_collection, message_output)

        elif user_input == "p":
            potion_selection_index += 1
            for sublist in item_hilite_coords_list:
                if "Potion" in sublist:
                    if potion_selection_index not in range(len(sublist[1])):
                        potion_selection_index = 0
            item_selection_msg_handler(item_hilite_coords_list, "Potion", potion_selection_index, items_collection, message_output)

        elif user_input == "j":
            use_item_handler(invt, "Weapon", item_hilite_coords_list, weapon_selection_index, prot_traits)
        elif user_input == "k":
            use_item_handler(invt, "Armor", item_hilite_coords_list, armor_selection_index, prot_traits)
        elif user_input == "l":
            use_item_handler(invt, "Potion", item_hilite_coords_list, potion_selection_index, prot_traits)

        elif user_input == "x":
            return None


def main ():
    #opening_screen.open_welcome_screen()
    #how_to_play_screen.how_to_play_screen()

    prot_name, prot_class = character_picking.pick_character()

    # load items that will be collectible from map
    items_collection = items.load_items()

    # load primary inventory
    invt = { "Weapon": {"Axe":1, "Knife":7 },
                "Potion": {"pot1":3 },
                "Armor": {"armor1":5 }
            }

    prot_traits = { "Lives":30, "Experience":7,
                    "Attack":5, "Defense":5, "Agility":5, "Strength":10,
                    "Load capacity":10 }

    firstkey = list(prot_class.keys())[0]

    prot_traits["Lives"] = prot_class[firstkey]["Lives"]
    prot_traits["Strength"] = prot_class[firstkey]["Strength"]
    prot_traits["Agility"] = prot_class[firstkey]["Agility"]

    prot_initial_coords = [ 105, 30 ]
    result = engage_level(invt, prot_traits, items_collection, "map_level_1.txt", prot_initial_coords)
    if result is None:
        print("Player interrupted the game.")
    else:
        if result == True:
            prot_initial_coords = [ 52, 2 ]
            result = engage_level(invt, prot_traits, items_collection, "map_level_2.txt", prot_initial_coords)
            if result is None:
                print("Player interrupted the game.")
            else:
                if result == True:
                    # engage cold warm hot
                    if hotwarm.play(10):
                        print("Congratulations! You have won!")
                    else:
                        print("We're sad that you've lost at the very end!")
                else:
                    print("You lost!")
        else:
            print("You lost!")

if __name__ == "__main__":
    main()
