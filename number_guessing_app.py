import tkinter as tk
from tkinter import messagebox
import random
import json
import os


# =========================================================
# SCORE FILE
# =========================================================

SCORE_FILE = "best_scores.json"


# =========================================================
# GAME DATA
# =========================================================

ranges = {
    "Easy": 50,
    "Medium": 100,
    "Hard": 500
}


# =========================================================
# LOAD BEST SCORES
# =========================================================

def load_scores():

    default_scores = {
        "Easy": None,
        "Medium": None,
        "Hard": None
    }

    if not os.path.exists(SCORE_FILE):
        return default_scores

    try:

        with open(SCORE_FILE, "r") as file:
            scores = json.load(file)

        # Make sure all required difficulty levels exist
        for level in default_scores:

            if level not in scores:
                scores[level] = None

        return scores

    except (json.JSONDecodeError, OSError, TypeError):

        return default_scores


best_scores = load_scores()

difficulty = "Easy"
secret_number = 0
attempts = 0


# =========================================================
# SAVE BEST SCORES
# =========================================================

def save_scores():

    try:

        with open(SCORE_FILE, "w") as file:
            json.dump(
                best_scores,
                file,
                indent=4
            )

    except OSError:

        messagebox.showerror(
            "Save Error",
            "Could not save your best scores."
        )


# =========================================================
# DIFFICULTY CHANGED
# =========================================================

def difficulty_changed(*args):

    global difficulty
    global secret_number
    global attempts

    difficulty = difficulty_var.get()

    maximum = ranges[difficulty]

    # Generate new secret number
    secret_number = random.randint(
        1,
        maximum
    )

    # Reset attempts
    attempts = 0

    # Update hint
    hint_label.config(
        text=f"Guess a number between 1 and {maximum}"
    )

    # Update result
    result_label.config(
        text=f"{difficulty} selected"
    )

    # Reset attempts
    attempts_label.config(
        text="Attempts: 0"
    )

    # Enable input
    guess_entry.config(
        state="normal"
    )

    # Enable check button
    guess_button.config(
        state="normal"
    )

    # Clear previous guess
    guess_entry.delete(
        0,
        tk.END
    )

    # Update best score
    if best_scores[difficulty] is None:

        best_label.config(
            text="Best Score: No score yet"
        )

    else:

        best_label.config(
            text=f"Best Score: {best_scores[difficulty]} attempts"
        )

    guess_entry.focus()


# =========================================================
# START NEW GAME
# =========================================================

def start_game():

    global secret_number
    global attempts
    global difficulty

    difficulty = difficulty_var.get()

    maximum = ranges[difficulty]

    # Generate random number
    secret_number = random.randint(
        1,
        maximum
    )

    # Reset attempts
    attempts = 0

    # Reset attempts display
    attempts_label.config(
        text="Attempts: 0"
    )

    # Reset hint
    hint_label.config(
        text=f"Guess a number between 1 and {maximum}"
    )

    # Reset result
    result_label.config(
        text="Game started! Make your guess."
    )

    # Enable input
    guess_entry.config(
        state="normal"
    )

    # Enable check button
    guess_button.config(
        state="normal"
    )

    # Clear old guess
    guess_entry.delete(
        0,
        tk.END
    )

    # Show best score
    if best_scores[difficulty] is None:

        best_label.config(
            text="Best Score: No score yet"
        )

    else:

        best_label.config(
            text=f"Best Score: {best_scores[difficulty]} attempts"
        )

    guess_entry.focus()


# =========================================================
# CHECK GUESS
# =========================================================

def check_guess():

    global attempts

    user_input = guess_entry.get().strip()

    # -----------------------------------------------------
    # EMPTY INPUT
    # -----------------------------------------------------

    if user_input == "":

        messagebox.showwarning(
            "Missing Guess",
            "Please enter a number."
        )

        guess_entry.focus()

        return

    # -----------------------------------------------------
    # CONVERT INPUT TO INTEGER
    # -----------------------------------------------------

    try:

        guess = int(user_input)

    except ValueError:

        messagebox.showwarning(
            "Invalid Input",
            "Please enter a valid whole number."
        )

        guess_entry.select_range(
            0,
            tk.END
        )

        guess_entry.focus()

        return

    # -----------------------------------------------------
    # CHECK RANGE
    # -----------------------------------------------------

    maximum = ranges[difficulty]

    if guess < 1 or guess > maximum:

        messagebox.showwarning(
            "Invalid Number",
            f"Please enter a number between 1 and {maximum}."
        )

        guess_entry.select_range(
            0,
            tk.END
        )

        guess_entry.focus()

        return

    # -----------------------------------------------------
    # COUNT ATTEMPT
    # -----------------------------------------------------

    attempts += 1

    attempts_label.config(
        text=f"Attempts: {attempts}"
    )

    # =====================================================
    # TOO LOW
    # =====================================================

    if guess < secret_number:

        difference = secret_number - guess

        # Easy mode: very close
        if difficulty == "Easy" and difference <= 5:

            result_label.config(
                text="⬆ Low — Very Close!"
            )

            hint_label.config(
                text="You're within 5 numbers! Try a little higher."
            )

        else:

            result_label.config(
                text="⬆ Too Low!"
            )

            hint_label.config(
                text=f"Try a higher number. Range: 1 - {maximum}"
            )

        guess_entry.select_range(
            0,
            tk.END
        )

        guess_entry.focus()

    # =====================================================
    # TOO HIGH
    # =====================================================

    elif guess > secret_number:

        difference = guess - secret_number

        # Easy mode: very close
        if difficulty == "Easy" and difference <= 5:

            result_label.config(
                text="⬇ High — Very Close!"
            )

            hint_label.config(
                text="You're within 5 numbers! Try a little lower."
            )

        else:

            result_label.config(
                text="⬇ Too High!"
            )

            hint_label.config(
                text=f"Try a lower number. Range: 1 - {maximum}"
            )

        guess_entry.select_range(
            0,
            tk.END
        )

        guess_entry.focus()

    # =====================================================
    # CORRECT ANSWER
    # =====================================================

    else:

        result_label.config(
            text="🎉 Correct!"
        )

        hint_label.config(
            text=f"You found the number in {attempts} attempts!"
        )

        # Update best score
        update_best_score()

        # Disable input
        guess_entry.config(
            state="disabled"
        )

        # Disable check button
        guess_button.config(
            state="disabled"
        )

        messagebox.showinfo(
            "Congratulations!",
            f"You guessed the number!\n\n"
            f"Number: {secret_number}\n"
            f"Attempts: {attempts}"
        )


# =========================================================
# UPDATE BEST SCORE
# =========================================================

def update_best_score():

    current_best = best_scores[difficulty]

    # -----------------------------------------------------
    # FIRST SCORE
    # -----------------------------------------------------

    if current_best is None:

        best_scores[difficulty] = attempts

        save_scores()

        best_label.config(
            text=f"Best Score: {attempts} attempts"
        )

        messagebox.showinfo(
            "New Best Score!",
            f"🏆 New best score!\n\n"
            f"{difficulty}: {attempts} attempts"
        )

    # -----------------------------------------------------
    # NEW BEST SCORE
    # -----------------------------------------------------

    elif attempts < current_best:

        best_scores[difficulty] = attempts

        save_scores()

        best_label.config(
            text=f"Best Score: {attempts} attempts"
        )

        messagebox.showinfo(
            "New Best Score!",
            f"🏆 New best score!\n\n"
            f"{difficulty}: {attempts} attempts"
        )

    # -----------------------------------------------------
    # NOT A BEST SCORE
    # -----------------------------------------------------

    else:

        best_label.config(
            text=f"Best Score: {current_best} attempts"
        )


# =========================================================
# SHOW BEST SCORES
# =========================================================

def show_scores():

    scores = ""

    for level, score in best_scores.items():

        if score is None:

            scores += f"{level}: No score yet\n"

        else:

            scores += f"{level}: {score} attempts\n"

    messagebox.showinfo(
        "Best Scores",
        scores
    )


# =========================================================
# EXIT GAME
# =========================================================

def exit_game():

    answer = messagebox.askyesno(
        "Exit Game",
        "Are you sure you want to exit?"
    )

    if answer:

        window.destroy()


# =========================================================
# MAIN WINDOW
# =========================================================

window = tk.Tk()

window.title(
    "Number Guessing Game"
)

window.geometry(
    "700x650"
)

window.minsize(
    600,
    550
)

window.configure(
    bg="#0B1220"
)


# =========================================================
# TITLE
# =========================================================

title_label = tk.Label(
    window,
    text="🎯 NUMBER GUESSING GAME",
    font=("Segoe UI", 26, "bold"),
    bg="#0B1220",
    fg="white"
)

title_label.pack(
    pady=(35, 10)
)


# =========================================================
# SUBTITLE
# =========================================================

subtitle_label = tk.Label(
    window,
    text="Guess the secret number!",
    font=("Segoe UI", 13),
    bg="#0B1220",
    fg="#AAB4C3"
)

subtitle_label.pack()


# =========================================================
# DIFFICULTY FRAME
# =========================================================

difficulty_frame = tk.Frame(
    window,
    bg="#172033"
)

difficulty_frame.pack(
    pady=30,
    padx=40,
    fill="x"
)


# =========================================================
# DIFFICULTY TITLE
# =========================================================

difficulty_title = tk.Label(
    difficulty_frame,
    text="Select Difficulty",
    font=("Segoe UI", 14, "bold"),
    bg="#172033",
    fg="white"
)

difficulty_title.pack(
    pady=(20, 10)
)


# =========================================================
# DIFFICULTY VARIABLE
# =========================================================

difficulty_var = tk.StringVar(
    value="Easy"
)


# =========================================================
# DIFFICULTY MENU
# =========================================================

difficulty_menu = tk.OptionMenu(
    difficulty_frame,
    difficulty_var,
    "Easy",
    "Medium",
    "Hard"
)

difficulty_menu.config(
    font=("Segoe UI", 12),
    width=15,
    bg="#26334D",
    fg="white",
    activebackground="#344563",
    activeforeground="white",
    relief="flat"
)

difficulty_menu["menu"].config(
    font=("Segoe UI", 12),
    bg="#26334D",
    fg="white"
)

difficulty_menu.pack(
    pady=(0, 20)
)


# =========================================================
# RANGE / HINT LABEL
# =========================================================

hint_label = tk.Label(
    window,
    text="Guess a number between 1 and 50",
    font=("Segoe UI", 13),
    bg="#0B1220",
    fg="#AAB4C3"
)

hint_label.pack(
    pady=5
)


# =========================================================
# GUESS ENTRY
# =========================================================

guess_entry = tk.Entry(
    window,
    font=("Segoe UI", 22),
    justify="center",
    width=12
)

guess_entry.pack(
    pady=15
)


# =========================================================
# CHECK GUESS BUTTON
# =========================================================

guess_button = tk.Button(
    window,
    text="CHECK GUESS",
    command=check_guess,
    font=("Segoe UI", 12, "bold"),
    bg="#3B82F6",
    fg="white",
    activebackground="#2563EB",
    activeforeground="white",
    relief="flat",
    padx=30,
    pady=10,
    cursor="hand2"
)

guess_button.pack(
    pady=5
)


# =========================================================
# RESULT LABEL
# =========================================================

result_label = tk.Label(
    window,
    text="Start the game!",
    font=("Segoe UI", 20, "bold"),
    bg="#0B1220",
    fg="white"
)

result_label.pack(
    pady=20
)


# =========================================================
# ATTEMPTS LABEL
# =========================================================

attempts_label = tk.Label(
    window,
    text="Attempts: 0",
    font=("Segoe UI", 13),
    bg="#0B1220",
    fg="#AAB4C3"
)

attempts_label.pack()


# =========================================================
# BEST SCORE LABEL
# =========================================================

best_label = tk.Label(
    window,
    text="Best Score: No score yet",
    font=("Segoe UI", 13, "bold"),
    bg="#0B1220",
    fg="#FFD166"
)

best_label.pack(
    pady=10
)


# =========================================================
# BUTTON FRAME
# =========================================================

button_frame = tk.Frame(
    window,
    bg="#0B1220"
)

button_frame.pack(
    pady=25
)


# =========================================================
# NEW GAME BUTTON
# =========================================================

new_game_button = tk.Button(
    button_frame,
    text="NEW GAME",
    command=start_game,
    font=("Segoe UI", 11, "bold"),
    bg="#26334D",
    fg="white",
    activebackground="#344563",
    activeforeground="white",
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2"
)

new_game_button.grid(
    row=0,
    column=0,
    padx=8
)


# =========================================================
# BEST SCORES BUTTON
# =========================================================

scores_button = tk.Button(
    button_frame,
    text="BEST SCORES",
    command=show_scores,
    font=("Segoe UI", 11, "bold"),
    bg="#26334D",
    fg="white",
    activebackground="#344563",
    activeforeground="white",
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2"
)

scores_button.grid(
    row=0,
    column=1,
    padx=8
)


# =========================================================
# EXIT BUTTON
# =========================================================

exit_button = tk.Button(
    button_frame,
    text="EXIT",
    command=exit_game,
    font=("Segoe UI", 11, "bold"),
    bg="#B83232",
    fg="white",
    activebackground="#8F2525",
    activeforeground="white",
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2"
)

exit_button.grid(
    row=0,
    column=2,
    padx=8
)


# =========================================================
# ENTER KEY
# =========================================================

window.bind(
    "<Return>",
    lambda event: check_guess()
)


# =========================================================
# DIFFICULTY CHANGE DETECTION
# =========================================================

difficulty_var.trace_add(
    "write",
    difficulty_changed
)


# =========================================================
# START FIRST GAME
# =========================================================

start_game()


# =========================================================
# RUN APPLICATION
# =========================================================

window.mainloop()