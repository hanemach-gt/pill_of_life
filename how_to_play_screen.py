import os

def how_to_play_screen(file_name =  "how_to_play_screen.txt"):
    os.system("clear")
    with open(file_name) as f:

        for line in f.readlines():
            os.system("sleep .2")
            for char in line:
                print(char, end="")
    print(end="")
