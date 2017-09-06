# def nameing_protagonist(protagonist_name):
#     # protagonist_name = input("How shall I call you?: ")
#     # print("Let it be, your's name is %s."% protagonist_name)
#     pass

# def pick_protagonist_class (protagonist_class):
print("""You can choose a three classes:  Gnom, Unicorn and Fairy.
[G]nom is big and strong. [U]nicorn healthy as a horse. [F]airy fast and courise""")

Gnom = {"strenght": 30, "agility": 10, "vitality": 20, }
Unicorn = {"strenght": 10, "agility": 20, "vitality": 30,}
Fairy = {"strenght": 20, "agility": 30, "vitality": 10,}

while True:
    player_class_choice = input("""Deside now, who you want to be [G], [U], [F]? : """)
    player_class_choice = player_class_choice.upper()

    if player_class_choice == "G":
        protagonist_class = Gnom
        break
    if player_class_choice == "U":
        protagonist_class = Unicorn
        break
    elif player_class_choice == "F":
        protagonist_class = Fairy
        break
    else:
        print("Error! I am afraid we have only three classes until next DLC, try again")

print("Great! you picked{0}".format())

# def main():
#     protagonist_class = pick_protagonist_class(protagonist_class)
#     protagonist_name = nameing_protagonist(protagonist_name)
#
#
# main()
