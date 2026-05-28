from tkinter import *
from functools import partial  # to prevent unwanted windows


class StartQuiz:
    """ Initial quiz interface (asks users how many questions they would like to answer) """

    def __init__(self):
        """Gets number of initial questions from user"""

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # strings for labels
        intro_string = ("In this quiz, you will have to answer questions based on the Japanese defense based martial art; Aikido. "
                        "\nThe questions will be on the practical translations of many different parts of Aikido. ")

        choose_string = "How many questions do you want to answer? (Maximum of 40)"

        # list of labels to be made (text | font | fg)
        start_labels_list = [
            ["Aikido Quiz", ("Arial", 16, "bold"), None],
            [intro_string, ("Arial", 12, "bold"), None],
            [choose_string, ("Arial", 12, "bold"), "#009900"]
        ]

        # create labels and add them to the reference list

        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1], fg=item[2],
                               wraplength=350, justify="left", padx=20, pady=10)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # extract choice label so that it can be changed to an error message if necessary.
        self.choose_label = start_label_ref[2]

        # frame so that entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_questions_entry = Entry(self.entry_area_frame, font=("Arial", 20, "bold"), width=10)
        self.num_questions_entry.grid(row=0, column=0, padx=10, pady=10)

        # create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"), fg="#FFFFFF",
                                  bg="#0057d8", text="Play", width=10, command=self.question_checker)
        self.play_button.grid(row=0, column=1)

    def question_checker(self):
        # error message
        has_errors = "no"
        max_questions = 40
        error = f"Please enter an integer more than 0 and less than {max_questions + 1}."

        # get requested amount of questions
        amt_requested = self.num_questions_entry.get()

        # reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", 12, "bold"))
        self.num_questions_entry.config(bg="#FFFFFF")

        # error checker
        try:
            # is integer?
            amt_requested = int(amt_requested)
            # make sure user response is within parameters
            if 0 < amt_requested <= max_questions:
                # success
                # invoke Play class with number of rounds
                Play(amt_requested)
                # hide root window (rounds choice)
                root.withdraw()
            else:
                # fail
                has_errors = "yes"

        except ValueError:
            # fail
            has_errors = "yes"

        # display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000", font=("Arial", 10, "bold"))
            self.num_questions_entry.config(bg="#F4CCCC")
            self.num_questions_entry.delete(0, END)


class Play:
    """ Interface for playing the Aikido Quiz itself """

    def __init__(self, how_many):
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.game_heading_label = Label(self.game_frame, text=f"Round 0 of {how_many}", font=("Arial", 16, "bold"))
        self.game_heading_label.grid(row=0)

        self.end_game_button = Button(self.game_frame, text="End Game", font=("Arial", 16, "bold"), fg="#FFFFFF",
                                      bg="#990000", width=10,
                                      command=self.close_play)
        self.end_game_button.grid(row=1)

    def close_play(self):
        # reshow root (choose rounds) and end current game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Aikido Quiz")
    StartQuiz()
    root.mainloop()

