def pick_character():
    protagonist_class = pick_protagonist_class()
    protagonist_name = nameing_protagonist()
    return protagonist_name, protagonist_class


def nameing_protagonist ():
    protagonist_name = input("How shall I call you?: ")
    print("Let it be, your name is %s."% protagonist_name)
    return protagonist_name


def pick_protagonist_class ():
    print("""You can choose one of three heroes:  Gnome, Unicorn and Fairy.
    [G]nome is big and strong. [U]nicorn is healthy as a horse. [F]airy is fast and courise""")

    heroes_to_pick = [
        {"Gnome" : {"Strength": 30, "Agility": 10, "Vitality": 20}},
        {"Unicorn": {"Strength": 10, "Agility": 20, "Vitality": 30}},
        {"Fairy": {"Strength": 20, "Agility": 30, "Vitality": 10}}
    ]

    while True:
        player_class_choice = input("""Decide now, who you want to be [G], [U], [F]? : """)
        player_class_choice = player_class_choice.upper()

        if player_class_choice == "G":
            hero = heroes_to_pick[0]
            for k, v in hero.items():
                print("Great! you picked {0} = {1}".format(k,v))
            return hero

        elif player_class_choice == "U":
            hero = heroes_to_pick[1]
            for k, v in hero.items():
                print("Great! you picked {0} = {1}".format(k,v))
            return hero

        elif player_class_choice == "F":
            hero = heroes_to_pick[2]
            for k, v in hero.items():
                print("Great! you picked {0} = {1}".format(k,v))
            return hero
        else:
            print("Error! I am afraid we have only three heroses, until next DLC, try again")





def main():
    protagonist_name, protagonist_class = pick_character()


if __name__ == "__main__": main()
