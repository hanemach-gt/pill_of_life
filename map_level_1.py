def map_level(file_name = "map_level_1.txt"):

    black='\033[30m'
    red='\033[31m'
    green='\033[32m'
    orange='\033[33m'
    blue='\033[34m'
    purple='\033[35m'
    cyan='\033[36m'
    lightgrey='\033[37m'
    darkgrey='\033[90m'
    lightred='\033[91m'
    lightgreen='\033[92m'
    yellow='\033[93m'
    lightblue='\033[94m'
    pink='\033[95m'
    lightcyan='\033[96m'


    with open(file_name) as f:
        for lines in f.readlines():
            for char in lines:
                if char == "<":
                    print(lightgreen, end="")
                if char == "#":
                    print(red, end="")
                if char == "~":
                    print(orange, end="")
                print(char, end="")


map_level()
