def nameing_protagonist():
    protagonist_name = input("How shall I call you?: ")
    print("Let it be, your name is %s."% protagonist_name)
    return protagonist_name

def pick_protagonist_class ():
    print("""You can choose a three heroses:  Gnom, Unicorn and Fairy.
    [G]nom is big and strong. [U]nicorn healthy as a horse. [F]airy fast and courise""")

    heroses_to_pick =[
    {"Gnom" : {"strenght": 30, "agility": 10, "vitality": 20}},
    {"Unicorn": {"strenght": 10, "agility": 20, "vitality": 30}},
    {"Fairy": {"strenght": 20, "agility": 30, "vitality": 10}}
    ]

    while True:
        player_class_choice = input("""Deside now, who you want to be [G], [U], [F]? : """)
        player_class_choice = player_class_choice.upper()

        if player_class_choice == "G":
            hero = heroses_to_pick[0]
            for k, v in hero.items():
                print("Great! you picked {0} = {1}".format(k,v))
            return hero
            break

        if player_class_choice == "U":
            hero = heroses_to_pick[1]
            for k, v in hero.items():
                print("Great! you picked {0} = {1}".format(k,v))
            return hero
            break

        elif player_class_choice == "F":
            hero = heroses_to_pick[2]
            for k, v in hero.items():
                print("Great! you picked {0} = {1}".format(k,v))
            return hero
            break
        else:
            print("Error! I am afraid we have only three heroses, until next DLC, try again")





    protagonist_class = pick_protagonist_class()
    protagonist_name = nameing_protagonist()
