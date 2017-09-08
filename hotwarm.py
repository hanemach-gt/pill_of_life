import random

def randomize_number():
    numbers = list(range(1, 10))
    randomized = []
    for k in range(3):
        index = random.randint(0, len(numbers)-1)
        randomized.append(str(numbers.pop(index)))

    return randomized

def validate_input(user_input):
    for i in range(len(user_input)):
        if user_input.count(user_input[i]) != 1:
            return False
    return True

def play(attempts):
    is_guessed = False
    count = 0
    digits_guessed = [False, False, False]
    randomized = randomize_number()
    while not is_guessed:
        count += 1
        if count >= attempts:
            print("You've exhausted your allowed attempts! You lost!")
            return False

        print("Guess #" + str(count))
        user_input = input("Enter your guess:")
        user_input = list(user_input)

        is_sequence_valid = validate_input(user_input)
        if not is_sequence_valid:
            print("Wrong value")
            continue

        if len(user_input) != len(randomized):
            print("Wrong value")
            continue

        for i in range(len(randomized) - 1, -1, -1):
            if user_input[i] not in randomized:
                print("cold")
            else:
                if user_input[i] == randomized[i]:
                    print("hot")
                    digits_guessed[i] = True
                else:
                    print("warm")

        if False not in digits_guessed:
            return True

    return False

def main():
    wants_to_play = True
    while wants_to_play:
        difficult = input("Enter\n\te - easy\n\tm - medium\n\th - hard")
        easy = 15
        medium = 10
        hard = 5
        attempts = 0
        if difficult == "e":
            attempts = easy
        elif difficult == "m":
            attempts = medium
        elif difficult == "h":
            attempts = hard

        play(attempts)
        ans = input("Do you still want to play? Y/n")
        if ans == "n":
            wants_to_play = False

if __name__ == "__main__": main()
