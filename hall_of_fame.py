import csv

def write_heigh_score(protagonist_name, exp, number_defeated_enemy,points, win_time = 0, file_name = "hall_of_fame.txt"):
    with open (file_name, "w", newline="") as new_file:
        score_file = csv.writer(new_file )
        high_score_values = [protagonist_name, int(exp), int(number_defeated_enemy), int(exp + number_defeated_enemy), win_time]
        high_score_headers = ["player name", "expierience", "number defeated enemy", "points", "win_time"]
        #high_score = list(zip(high_score_headers, high_score_values))
        # for elemet in high_score:
        #     for k in elemet:
        #         print("".join(k))

        score_file.writerow(high_score_headers)
        score_file.writerow(high_score_values.format(protagonist_name, int(exp), int(number_defeated_enemy), int(exp + number_defeated_enemy), win_time)


write_heigh_score("Pepik", 123, 50, 123 + 50, 0)
