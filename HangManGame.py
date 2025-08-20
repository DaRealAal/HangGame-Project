# import the libraries that needed
import random
import time
import threading
from HangmanArt import hangman_ASCII_art
from random import randint
from time import sleep as time_sleep
from colorama import Fore

# cool colors for this terminal
ANSI_colors = {
    "red": Fore.RED,
    "green": Fore.GREEN,
    "blue": Fore.BLUE,
    "reset": Fore.RESET,
}

# initialize the variables
letters_guessed = set()
is_guessed = False
wrong_guess = 0
lives = 5
correct_guess = 0
seconds_timer = 0
display_timer = f"00:00:00"
player_name = ""
guess = ""


# creates the timer to count up
def timer(secs):
    global display_timer
    while secs >= 0:
        second = secs % 60
        minute = round(secs / 60) % 60
        hour = round(secs / 3600) % 60

        display_timer = f"{hour}:{minute}:{second}"
        time.sleep(1)
        secs += 1

    return display_timer


# it prints as if something is typing it out
def print_slow(text):
    for letter in text:
        print(letter, end="", flush=True)
        time_sleep(0.1)


# starts the game function
def start_game():
    # ensuring that variables can be accessed
    global guess, lives, wrong_guess, correct_guess, is_guessed, random_word
    print_slow("Enter your name: ")
    player_name = input()
    print_slow("Welcome " + player_name + "!\n")
    random_word = random_word_file()
    secret_word_length = len(random_word)
    guess_words_length = 0

    # loops terminate only if the player didn't guess the word properly or got it wrong
    while lives > 0 and not is_guessed:
        threading.Thread(target=timer, args=(seconds_timer,), daemon=True).start()

        # if the output is correct random_word to display properly then is_guessed is 'true'
        if random_word == show_letter():
            is_guessed = True
            break

        print_slow(
            f"Correct letters: {correct_guess} | Wrong letters: {wrong_guess} | Lives: {lives}\n"
        )
        print(show_art())
        print_slow(show_letter() + "\n\n")
        print_slow("Enter letter/word: ")
        guess = input()

        # cheching if the letters are numeric values
        if guess.isnumeric():
            print(
                ANSI_colors["red"]
                + "Please enter only text/letter"
                + ANSI_colors["reset"]
            )
            continue
        # if the user has already wrote the correct word with requirement condition statement
        # then yes, is_guessed equals 'True'
        elif guess == random_word or (
            guess_words_length >= secret_word_length and show_letter() == random_word
        ):
            is_guessed = True
        # checks if the guess letter is included in the random_word
        elif guess in random_word:
            # spliting each word to count the correct letters
            letters_split_length = len(list(guess))
            correct_guess += letters_split_length
            secret_word_length += letters_split_length
            guess_words_length += 1
            for letter in guess:
                letters_guessed.add(letter)
            letters_split_length = 0
            continue
        else:
            # each letters are not correct so therefore we count the wrong words to wrong_guess
            letters_split_length = len(list(guess))
            wrong_guess += letters_split_length
            lives -= 1
            # random letter_added for hint is only conditioned true if being added
            letter_added = False
            # loops unitl a word is added to the output blinks and not the repeated words
            while not letter_added:
                added_letter = random_word[randint(0, len(random_word) - 1)]
                if not added_letter in letters_guessed:
                    letters_guessed.add(added_letter)
                    letter_added = True
                else:
                    continue
            # resets to zero so that other if statement can count
            letters_split_length = 0

    # finally I'm cheching if the user did actually guess the word correctly
    if is_guessed:
        print_slow(
            "{}{}{}".format(
                ANSI_colors["green"],
                f"Congrats the word was {random_word}",
                ANSI_colors["reset"] + "\n",
            )
        )

        print_slow("It took you {}\n".format(display_timer))
    else:
        print_slow("Sorry the word was " + random_word + ".\n")


# randomized a word from a words.txt file
def random_word_file() -> str:
    secret_words = list()
    with open("words.txt", "r") as file:
        words = file.readlines()
        for word in words:
            secret_words.append(word.strip())
    return random.choice(secret_words)


# display the letters to the user
def show_letter():
    output = ""
    for letter in random_word:
        if letter in letters_guessed:
            output += letter
        elif letter == " ":
            output += " "
        else:
            output += "_"
    return output


# art from the HangmanArt.py
def show_art():
    # everytime if the user guesses the wrong letter then the body parts is revealed each time
    match wrong_guess:
        case 0:
            return hangman_ASCII_art.hangman_art_1
        case 1:
            return hangman_ASCII_art.hangman_art_2
        case 2:
            return hangman_ASCII_art.hangman_art_3
        case 3:
            return hangman_ASCII_art.hangman_art_4
        case 4:
            return hangman_ASCII_art.hangman_art_5
        case 5:
            return hangman_ASCII_art.hangman_art_6
        case 6:
            return hangman_ASCII_art.hangman_art_7


# the only file that is currently running
if __name__ == "__main__":
    # timer is running in the background
    game = threading.Thread(target=start_game)
    game.start()
    game.join()
    print_slow("Thank you for playing this game")