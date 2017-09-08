import csv

def write_heigh_score(protagonist_name, exp, defeated_enemy, victory_time = 0, file_name = "hall_of_fame.txt"):
    with open (file_name, "w", newline="") as new_file:
        width = 5
        values = [protagonist_name, exp, defeated_enemy, victory_time]
        headers = ["player_name","expierience", "defeated_enemy","victory_time"]
        scores = list(zip(headers, values))
        #configure writer to write standard csv file
        writer = csv.writer(new_file)
        #writer.writerow(["player_name"," "*(len(values[0])-len(headers[0])),"expierience"," "*(len(values[0])-len(headers[0]))])
        writer.writerow(["|{:^40}|{:^40}|{:^40}|{:^40}|".format("player_name","expierience", "defeated_enemy","victory_time")])
        writer.writerow(["|{:^40}|{:^40}|{:^40}|{:^40}|".format(protagonist_name, exp, defeated_enemy, victory_time)])
        print(len(protagonist_name))







write_heigh_score("de", "1", "5hhhhhhhhhhhh0", "hhhhhhhhhhhhhh0",)
