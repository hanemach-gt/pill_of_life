# appends keys and values from inventory[masterkey] nicely converted to string to invtable,
# indenting with item_indent, aligning to max_width
# appends coordinates of items in resulting inventory table for highlighting to
# item_hilite_coords_list, using invt_ypos as frame of reference
def batch_item_append (inventory, masterkey, invtable, item_indent, max_width, invt_ypos, item_hilite_coords_list):
    subinventory = inventory[masterkey]
    keys = sorted(list(subinventory.keys()))
    hilite_list = []
    for i in range(len(keys)):
        no = "#" + str(i+1)
        key_len = len(keys[i])
        amount = subinventory[keys[i]]
        amount_len = len(str(subinventory[keys[i]]))
        spaces_between_key_value = max_width - (len(item_indent) + len(no) + 1 + amount_len + len(keys[i]) + 1)

        invtable.append(item_indent + list(no) + [" "] + list(keys[i]) + [" "] * spaces_between_key_value + list(str(amount)) + [" "])
        # preserve: key, y coord of hilite start, x begin of hilite, length of hilite
        hilite_list.append([keys[i], invt_ypos[0], len(item_indent)+1, max_width - (len(item_indent) + 1)])
        # 3rd element of list appended in the list above is incremented by one
        # additionally because we `embrace` our inventory table between
        # '[' ']', which added one charcter in front of every line
        invt_ypos[0] += 1

    item_hilite_coords_list.append([masterkey, hilite_list])

# appends nicely converted trait to inventory table, aligning to max_width
def trait_append(prot_traits, trait, invtable, max_width):
    key_len = len(trait)
    val_len = len(str(prot_traits[trait]))
    invtable.append(["  "] + list(trait) + [" "] * (max_width - (key_len + val_len + 3)) + list(str(prot_traits[trait])) + [" "])

def generate_inventory_table(inventory, item_hilite_coords_list, prot_traits, max_width=25):

    invtable = []
    item_hilite_coords_list.clear()

    str_inventory = " Available items: "
    str_weapons = "[I] Weapons:  [J]-remove"
    str_armor = "[O] Armor:  [K]-remove"
    str_potions = "[P] Potions:  [L]-use"
    str_none = "[empty]"

    item_indent = [" "] * 3

    line_none = item_indent + list(str_none) + [" "] * (max_width - (len(str_none) + len(item_indent)))

    empty_line = [" "] * max_width

    invt_ypos = [0]
    invtable.append(empty_line)
    invtable.append(list(str_inventory) + [" "] * (max_width - len(str_inventory)))
    invt_ypos[0] += 2

    invtable.append(empty_line)
    invtable.append(list(str_weapons) + [" "] * (max_width - len(str_weapons)))
    invtable.append(empty_line)
    invt_ypos[0] += 3
    # enumerate weapons
    if "Weapon" not in inventory:
        invtable.append(line_none)
        invt_ypos[0] += 1
    else:
        batch_item_append(inventory, "Weapon", invtable, item_indent, max_width, invt_ypos, item_hilite_coords_list)

    invtable.append(empty_line)
    invtable.append(list(str_armor) + [" "] * (max_width - len(str_armor)))
    invtable.append(empty_line)
    invt_ypos[0] += 3
    # enumerate armor
    if "Armor" not in inventory:
        invtable.append(line_none)
        invt_ypos[0] += 1
    else:
        batch_item_append(inventory, "Armor", invtable, item_indent, max_width, invt_ypos, item_hilite_coords_list)

    invtable.append(empty_line)
    invtable.append(list(str_potions) + [" "] * (max_width - len(str_potions)))
    invtable.append(empty_line)
    invt_ypos[0] += 3
    # enumerate potions
    if "Potion" not in inventory:
        invtable.append(line_none)
        invt_ypos[0] += 1
    else:
        batch_item_append(inventory, "Potion", invtable, item_indent, max_width, invt_ypos, item_hilite_coords_list)

    invtable.append(empty_line)
    invt_ypos[0] += 2

    str_stats = " Hero statistics:"
    invtable.append(list(str_stats) + [" "] * (max_width - len(str_stats)))
    invtable.append(empty_line)
    invt_ypos[0] += 2

    # not added in batch to enforce arbitrary order of appending
    trait_append(prot_traits, "Load capacity", invtable, max_width)
    trait_append(prot_traits, "Experience", invtable, max_width)
    trait_append(prot_traits, "Attack", invtable, max_width)
    trait_append(prot_traits, "Defense", invtable, max_width)
    trait_append(prot_traits, "Lives", invtable, max_width)
    trait_append(prot_traits, "Strength", invtable, max_width)
    trait_append(prot_traits, "Agility", invtable, max_width)

    invtable.append(empty_line)

    # embrace inventory table with '[' ']'
    for i in range(len(invtable)):
        invtable[i] = ["["] + invtable[i] + ["]"]

    return invtable

def main():
    items = { "Weapon": {"Axe":1, "Knife":7},
                "Potion": {},
                "Armor": {}
            }
    item_hilite_coords_list = []
    invtable = generate_inventory_table(items, item_hilite_coords_list)

    for li in item_hilite_coords_list:
        print(li)

if __name__ == "__main__": main()
