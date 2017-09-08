import random
from character_picking import*
level_changer = 0


protagonist_name = nameing_protagonist()
protagonist_class = pick_protagonist_class()

print(protagonist_name)
for i in protagonist_class:
    for k,v in i.tems():
        print(k,v)
def create_antagonist():
    anta_strenght = random.randint(1,30) + level_changer
    anta_agility = random.randint(1, 30)
    anta_health_points = random.randint(1,30)



# def action_test_prot():
#     test_prot = random.randint(1,100)
#     return test_prot
#
#
# def action_test_anta():
#     test_anta = random.randint(1,100)
#     return test_anta
#
#
# def damage_points_prot(prot_strenght, weapon_attack):
#         prot_demage_points = prot_strenght + weapon_attack
#         print(prot_demage_points, type(prot_demage_points))
#         return prot_demage_points
#
#
# def demage_points_anta(anta_strenght):
#         anta_demage_points = anta_strenght
#         print(anta_demage_points, type(anta_demage_points))
#         return anta_demage_points
#
#
#
#     # prot_health_points = 30
#     # prot_strenght = 1
#     # prot_agility = 5
#     # weapon_attack = 5
#     #
#     # anta_agility = 5
#     # anta_health_points = 30
#     # anta_strenght = 5
#
#     anta_demage_points = demage_points_anta(anta_strenght)
#     prot_demage_points = damage_points_prot(prot_strenght, weapon_attack)
#
#
# def fight(prot_health_points, anta_health_points, anta_demage_points, prot_demage_points):
#
#     if prot_agility <= anta_agility:
#         while prot_health_points > 0 or anta_health_points > 0:
#             if action_test_anta() > 50:
#                 prot_health_points -= anta_demage_points
#             else:
#                 print("miss")
#             if action_test_prot() > 49:
#                 anta_health_points -= prot_demage_points
#                 print()
#             else:
#                 print("miss")
#             if anta_health_points == 0:
#                print("win!")
#                break
#             if prot_health_points == 0:
#                 print("lose")
#                 break
#     else:
#         while prot_health_points > 0 or anta_health_points > 0:
#             if action_test_prot() > 49:
#                 anta_health_points -= prot_demage_points
#                 print()
#             else:
#                 print("miss")
#             if action_test_anta() > 50:
#                 prot_health_points -= anta_demage_points
#             else:
#                 print("miss")
#             if anta_health_points == 0:
#                print("win!")
#                break
#             if prot_health_points == 0:
#                 print("lose")
#                 break
#
