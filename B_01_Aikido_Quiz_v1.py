from tkinter import *
from functools import partial  # to prevent unwanted windows
import csv
import random

def get_question_answer():
    # retrieve colours from csv file and put them in a list
    file = open("Aikido Quiz Database.csv", "r")
    all_questions = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row
    all_questions.pop(0)

    answer_options = []

    # pick a question
    quiz_question_chosen = random.choice(all_questions)

    # loop until we have three incorrect options
    while len(answer_options) < 3:
        potential_option = random.choice(all_questions)
        if potential_option[2] in answer_options or potential_option == quiz_question_chosen:
            print(potential_option)
        else:
            answer_options.append(potential_option[2])

    # add correct answer to a random place in the answer options
    answer_options.insert(random.randint(0, 4), quiz_question_chosen[2])


class StartQuiz:
    """ Initial quiz interface (asks users how many questions they would like to answer) """

    def __init__(self):
        """Gets number of initial questions from user"""

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # strings for labels
        intro_string = ("In this quiz, you will have to answer questions based on the Japanese defense based martial \n"
                        "art Aikido. The questions will be on the practical translations of many different parts of Aikido. ")

        choose_string = "How many questions do you want to answer? (Maximum of 40)"

        # list of labels to be made (text | font | fg)
        start_labels_list = [
            ["Aikido Quiz", ("Arial", 16, "bold"), None],
            [intro_string, ("Arial", 12), None],
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
        self.choose_label.config(text="How many questions do you want to answer? (Maximum of 40)", fg="#009900", font=("Arial", 12, "bold"))
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
    """ Interface for playing the colour quest game """

    def __init__(self, how_many):
        self.play_box = Toplevel()

        self.quiz_frame = Frame(self.play_box)
        self.quiz_frame.grid(padx=10, pady=10)

        # body font for most labels
        body_font = ("Arial", 12)

        # list for label details (text | font | background | row)
        play_labels_list = [
            ["Aikido Quiz", ("Arial", 16, "bold"), None, 0],
            ["Question # out of #", body_font, "#FFF2CC", 1],
            ["Question goes here", ("Arial", 14), "#D5E8D4", 2],
            ["You chose, result", body_font, "#D5E8D4", 4]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.quiz_frame, text=item[0], font=item[1], bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(item)

        # retrieve labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.target_label = play_labels_ref[1]
        self.results_label = play_labels_ref[3]

        # set up colour buttons
        self.colour_frame = Frame(self.quiz_frame)
        self.colour_frame.grid(row=3)

        # create 4 buttons in a 2x2 grid
        for item in range(0, 4):
            self.colour_button = Button(self.colour_frame, font=body_font, text="Option Name", width=15)
            self.colour_button.grid(row=item // 2, column=item % 2, padx=5, pady=5)

        # frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.quiz_frame)
        self.hints_stats_frame.grid(row=6)

        # list for buttons (frame | text | bg | command | width | row | column)
        control_button_list = [
            [self.quiz_frame, "Next Question", "#0057D8", "", 21, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", "", 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#333333", "", 10, 0, 1],
            [self.quiz_frame, "End", "#990000", self.close_play, 21, 7, None]
        ]

        # create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2], command=item[3], font=("Arial", 16, "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)


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

