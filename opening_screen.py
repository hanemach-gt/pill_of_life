import os

def open_welcome_screen(file_name =  "welcome_screen.txt"):
    with open(file_name) as f:

        for line in f.readlines():
            os.system("sleep .02")
            for char in line:
                print(char, end="")
    print(end="")
    os.system("sleep 2.5")
