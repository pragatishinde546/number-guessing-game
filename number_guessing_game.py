import random


# Best scores for each difficulty
best_scores = {
    "Easy": None,
    "Medium": None,
    "Hard": None
}


def choose_difficulty():
    """Let the player choose a difficulty level."""

    print("\nChoose Difficulty:")
    print("1. Easy   (1 - 50)")
    print("2. Medium (1 - 100)")
    print("3. Hard   (1 - 500)")

    while True:
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            return "Easy", 50

        elif choice == "2":
            return "Medium", 100

        elif choice == "3":
            return "Hard", 500

        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")


def play_game(difficulty, maximum):
    """Run one complete guessing game."""

    number = random.randint(1, maximum)
    attempts = 0

    print("\n--------------------------------")
    print(f"Difficulty: {difficulty}")
    print(f"I'm thinking of a number between 1 and {maximum}.")
    print("--------------------------------")

    while True:

        try:
            guess = int(input("Enter your guess: "))

        except ValueError:
            print("❌ Please enter a valid number.")
            continue

        if guess < 1 or guess > maximum:
            print(f"⚠️ Please enter a number between 1 and {maximum}.")
            continue

        attempts += 1

        if guess < number:
            print("⬆️ Too low! Try a higher number.")

        elif guess > number:
            print("⬇️ Too high! Try a lower number.")

        else:
            print("\n🎉 Congratulations!")
            print(f"You guessed the number {number}!")
            print(f"Attempts: {attempts}")

            return attempts


def update_best_score(difficulty, attempts):
    """Update the best score if the current score is better."""

    if best_scores[difficulty] is None:
        best_scores[difficulty] = attempts
        print("🏆 New best score!")

    elif attempts < best_scores[difficulty]:
        best_scores[difficulty] = attempts
        print("🏆 New best score!")

    else:
        print(f"Best score: {best_scores[difficulty]} attempts")


def show_best_scores():
    """Display all best scores."""

    print("\n========== BEST SCORES ==========")

    for difficulty, score in best_scores.items():

        if score is None:
            print(f"{difficulty}: No score yet")

        else:
            print(f"{difficulty}: {score} attempts")

    print("=================================")


def main():
    """Main program."""

    print("\n======================================")
    print("       🎯 NUMBER GUESSING GAME")
    print("======================================")

    while True:

        difficulty, maximum = choose_difficulty()

        attempts = play_game(difficulty, maximum)

        update_best_score(difficulty, attempts)

        show_best_scores()

        while True:

            play_again = input("\nDo you want to play again? (y/n): ").strip().lower()

            if play_again == "y":
                break

            elif play_again == "n":
                print("\n======================================")
                print("      Thanks for playing! 👋")
                print("======================================")
                return

            else:
                print("❌ Please enter 'y' or 'n'.")


# Start the game
if __name__ == "__main__":
    main()