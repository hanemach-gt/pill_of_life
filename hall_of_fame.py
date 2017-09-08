import csv

def write_heigh_score(protagonist_name, exp, defeated_enemy, victory_time = 0, file_name = "hall_of_fame.txt"):
    f = open(file_name, "w")

        f.write(["|{:^25}|{:^25}|{:^25}|{:^25}|{:^25}|".format
                        ("player_name", "expierience", "defeated_enemy", "points", "victory_time")
                        ])
with open (file_name, "w", newline="") as new_file:
    points = int(exp)+ int(defeated_enemy)
    points = str(points)
    values = [protagonist_name, exp, defeated_enemy, victory_time]
    # headers = ["player_name","expierience", "defeated_enemy","victory_time"]
    writer = csv.writer(new_file)

        writer.writerow(["|{:^25}|{:^25}|{:^25}|{:^25}|{:^25}|".format
                        (protagonist_name, exp, defeated_enemy, points, victory_time)
                        ])
        print(len(protagonist_name))








write_heigh_score("pepik", "10", "550", "10",)
