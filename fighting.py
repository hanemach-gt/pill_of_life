import random
import msg


def action_test_prot():
    test_prot = random.randint(1,100)
    return test_prot


def action_test_anta():
    test_anta = random.randint(1,100)
    return test_anta


def load_combat_values(invt, weapon_selection_index):
    weapon_attack = invt["Weapon"][weapon_selection_index]
    anta_strenght = 5

    anta_damage_points = anta_strenght
    prot_damage_points = prot_strenght + weapon_attack

    return anta_damage_points, prot_damage_points


def fight(prot_traits, antags_coords, antag_index, message_output, invt, weapon_selection_index):
    anta_damage_points, prot_damage_points = load_combat_values(invt, weapon_selection_index)

    if action_test_anta() > 50:
        prot_traits["Lives"] -= anta_damage_points
        msg.set_output_message(message_output, "You got hit  ")
    else:
        msg.set_output_message(message_output, "Missed anta hit  ")

    if action_test_prot() > 49:
        anta_health_points -= prot_damage_points
        msg.set_output_message(message_output, "Hit anta  ")
    else:
        msg.set_output_message(message_output, "Anta missed hit  ")
