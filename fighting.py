import random
import msg


def action_test_prot():
    test_prot = random.randint(1,100)
    return test_prot


def action_test_anta():
    test_anta = random.randint(1,100)
    return test_anta


def load_combat_values(invt, weapon_name, prot_traits):
    weapon_attack = 0
    if weapon_name:
        weapon_attack = invt["Weapon"][weapon_name]

    anta_strenght = 1
    prot_strenght = 0
    if "Strength" in prot_traits:
        prot_strenght = prot_traits["Strength"]

    anta_damage_points = anta_strenght
    prot_damage_points = prot_strenght + weapon_attack

    return anta_damage_points, prot_damage_points


def fight(prot_traits, antags_coords, antag_index, message_output, invt, weapon_name):
    anta_damage_points, prot_damage_points = load_combat_values(invt, weapon_name, prot_traits)

    if action_test_anta() > 50:
        prot_traits["Lives"] -= anta_damage_points
        msg.set_output_message(message_output, "You got hit  ")
    else:
        msg.set_output_message(message_output, "Cell miss hit  ")

    if action_test_prot() > 49:
        # apply damage to antagonist
        #antags_coords is a list of lists of form [[x,y], hp]
        antags_coords[antag_index][1] -= prot_damage_points
        msg.set_output_message(message_output, "You Hit antagonist  ")
    else:
        msg.set_output_message(message_output, "You missed hit  ")
