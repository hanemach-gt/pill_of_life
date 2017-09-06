def load_items(file_name="items.txt"):
    items = []
    with open(file_name) as file:
        for line in file:
            trio = line.split(",") #[type, item, trait1:delta1|...|traitn:deltan]
            trio[2] = trio[2].split("|") #[type, item, [trait1:delta1, ... traitn:deltan]
            for i in range(len(trio[2])): # iterate over traits
                trio[2][i] = trio[2][i].split(":")
                trio[2][i][1] = int(trio[2][i][1]) # convert delta to an int

            trio[2] = dict(trio[2])
            items.append(tuple(trio))

    # returns ((type1, item1, {trait1 : delta1, ... traitn : deltan}),
    #          (type2, item2, {trait2 : delta2, ... traitn : deltan}))
    return tuple(items)


def main():
    items = load_items()
    print(items)


if __name__ == "__main__": main()
