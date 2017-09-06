import time
import sys

def open_welcome_screen(file_name =  "welcome.txt"):
    f = open(file_name)

    o= "Hello there\n"
    for char in o:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.09)

    # for line in f.readlines():
    #     open_screen.append(line.strip("\n").split(""))

    # print(open_screen)

    f.close()

def main():

    open_welcome_screen()

main()
