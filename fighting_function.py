import random
def testing_fot_action():
    hit_test = random.randint(0,100)
    if hit_test <= 50:
        return True
    else:
        return False


def player_attacking(player_str, weapon_attack, enemy_health_points):
        player_damage = player_str + weapon_attack
    return player_damage

def enemy_attacking(enemy_str, player_health_points):
        enemy_damage = enemy_str
    return enemy_damage

def main():
    weapon_attack = 0
    player_str = 1
    player_health_points = 3
    enemy_str = 1
    enemy_health_points = 3
    player_damage =  player_attacking(player_str, weapon_attack, enemy_health_points)
    enemy_damage = enemy_attacking(enemy_str, player_health_points)

    while player_health_points > 0 or enemy_health_points > 0:
        if testing_fot_action:
            player_health_points -= enemy_damage
        enemy_health_points -= player_damage
        elif testing_fot_action:
            enemy_health_points -= player_damage


        # print(tourns)
        # if enemy_health_points <= 0:
        #     print("you have won")
        #     break
        # elif player_health_points <= 0:
        #     print("enemy win")
        #     break
        # if tourns == 4:
        #     print("infiniteloop")
        #     break
main()
