def load_file(filename="hall_of_fame.txt"):
    hof = []
    try:
        with open(filename) as f:
            for line in f:
                record = line.strip()
                record = record.split(",")
                hof.append(record)

    except FileNotFoundError:
        print("Cound not load Hall of Fame")

    return hof


def save_file(hof, filename="hall_of_fame.txt"):
    try:
        with open(filename, "w") as f:
            for entry in hof:
                f.write(entry[0] + "," + entry[1] + "\n")

    except IOError:
        print("Could not save Hall of Fame")


def sort_hof(hof):
    for i in range(len(hof)):
        for j in range(len(hof)-1):
            if int(hof[j+1][1]) < int(hof[j][1]):
                swap = hof[j+1]
                hof[j+1] = hof[j]
                hof[j] = swap

    return hof

def print_hof(hof):
    maxnamelen = 0
    for record in sort_hof(hof):
        if len(record[1]) > maxnamelen:
            maxnamelen = len(record[1])

    player_str = "player name"
    namecollen = max(len(player_str), maxnamelen)

    print(player_str + " " * (len(player_str) - namecollen) + "|time")
    for record in hof:
        print(record[0] + " " * (namecollen - len(record[0])) + "|" + record[1])

def main():
    hof = load_file()
    print_hof(hof)

if __name__ == "__main__": main()
