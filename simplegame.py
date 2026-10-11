import random

def guess_the_number():
    secret_number = random.randint(1, 20)
    attempts = 0
    max_attempts = 5

    print("Welcome to Guess the Number!")
    print("I picked a number between 1 and 20.")
    print(f"You have {max_attempts} attempts to guess it.\n")

    while attempts < max_attempts:
        try:
            guess = int(input("Enter your guess: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        attempts += 1

        if guess < secret_number:
            print("Too low! Try a higher number.")
        elif guess > secret_number:
            print("Too high! Try a lower number.")
        else:
            print(f"Correct! You guessed the number in {attempts} attempts.")
            return

    print(f"Game over! The number was {secret_number}.")

guess_the_number()