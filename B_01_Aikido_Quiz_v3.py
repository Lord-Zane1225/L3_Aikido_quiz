from tkinter import *
from functools import partial  # to prevent unwanted windows
import random


def get_question_answer (all_questions):
    """ Get 1 question and 3 options for the quiz from the database """

    answer_options = []
    to_return = []
    quiz_question_chosen_func = random.choice(all_questions)

    # remove used question to prevent duplicates
    all_questions.remove(quiz_question_chosen_func)

    # loop until we have three incorrect options
    while len(answer_options) < 3:
        potential_option = random.choice(all_questions)
        if potential_option[1] not in answer_options:
            answer_options.append(potential_option[1])

    # add correct answer to a random place in the answer options
    answer_options.insert(random.randint(0, 4), quiz_question_chosen_func[1])

    # return question and options
    for item in quiz_question_chosen_func:
        to_return.append(item)
    for item in answer_options:
        to_return.append(item)
    return to_return


class StartQuiz:
    """ Initial quiz interface (asks users how many questions they would like to answer) """

    def __init__(self):
        """Gets number of initial questions from user"""

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # strings for labels
        intro_string = ("In this quiz, you will have to answer questions based on the Japanese defense based martial \n"
                        "art Aikido. The questions will be on the practical translations of many different parts of Aikido. ")

        choose_string = "How many questions do you want to answer? (Maximum of 41)"

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
        max_questions = 41
        error = f"Please enter an integer more than 0 and less than {max_questions + 1}."

        # get requested amount of questions
        amt_requested = self.num_questions_entry.get()

        # reset label and entry box (for when users come back to home screen)
        self.choose_label.config(text="How many questions do you want to answer? (Maximum of 41)", fg="#009900", font=("Arial", 12, "bold"))
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

        # Integers / String Variables
        # rounds played - start with zero
        self.questions_attempted = IntVar() # rounds_played in colour quest
        self.questions_attempted.set(0)

        self.questions_wanted = IntVar() # rounds_wanted
        self.questions_wanted.set(how_many)

        self.questions_correct = IntVar()
        self.questions_correct.set(0)

        # lists
        # hard coded questions to prevent quiz from crashing (rather than using a csv)
        all_questions = [['Enemi', 'Sliding step'], ['Ayumi ashi', 'Stepping across'], ['Tenkai', '180 turn'],
                         ['Tenkan', '180 turn, foot follows'], ['Irimi tenkan', 'Step, 180, foot follows'],
                         ['Hantai ten kan', '90 turn'], ['Ukemi', 'Roll'], ['Ski', 'Jab'], ['Shiko', 'Knee walking'],
                         ['Ikkyo', 'First pin'], ['Nikkyo', 'Second pin'], ['Sankkyo', 'Third pin'],
                         ['Yonkkyo', 'Fourth pin'], ['Gokkyo', 'Fifth pin'], ['Shihonage', 'Throw of four directions'],
                         ['Iriminage', 'Entering throw'], ['Kokyuho', 'Breathing throw'],
                         ['Kotegeashi', 'Throw by twisting the wrist'], ['Taisubaki', 'Footwork'],
                         ['Shomenuchi', 'Chopping strike'], ['Katate dori', 'Mirrored grab'],
                         ['Ryotedori', 'Two handed grab'], ['Kata dori', 'Clothing grab'], ['Mai', 'Forwards'],
                         ['Ushero', 'Backwards'], ['Nage', 'Thrower'], ['Uke', 'Faller'], ['Seiza', 'Seated on knees'],
                         ['Keiza', 'Seated on knees, toes up'], ['Rei', 'Bow'], ['Omote', 'In front'],
                         ['Ura', 'Behind'], ['Morote dori', 'Two to one grab'],
                         ['Ushero ryotedori', 'Behind, two handed grab'], ['Sensei', 'Teacher'],
                         ['Shihan', 'Master teacher'], ['Shoman', 'Founder'], ['Onegaishimasu', 'I humbly request'],
                         ['Domo arigato gozaimasu', 'Thank you very much'],
                         ['Aikido', 'Way of unifying with the spirit']]

        self.question_and_answer_list = []

        self.play_box = Toplevel()

        self.quiz_frame = Frame(self.play_box)
        self.quiz_frame.grid(padx=10, pady=10)

        # if users press the 'x' on the game window, end the entire game
        self.play_box.protocol('WM_DELETE_WINDOW', root.destroy)

        # body font for most labels
        body_font = ("Arial", 12)

        # list for label details (text | font | background | row)
        play_labels_list = [
            ["Aikido Quiz", ("Arial", 16, "bold"), None, 0],
            ["Question # out of #", body_font, "#FFF2CC", 1],
            ["What is the practical translation for\n#?", ("Arial", 14), "#D5E8D4", 2],
            ["You chose, result", body_font, "#D5E8D4", 4]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.quiz_frame, text=item[0], font=item[1], bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(self.make_label)

        # retrieve labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.target_label = play_labels_ref[1]
        self.question_label = play_labels_ref[2]
        self.results_label = play_labels_ref[3]

        # set up option buttons
        self.option_frame = Frame(self.quiz_frame)
        self.option_frame.grid(row=3)

        self.option_button_ref = []

        # create 4 buttons in a 2x2 grid
        for item in range(0, 4):
            self.option_button = Button(self.option_frame, font=body_font, text="Option Name", width=15, height=2,
                                        wraplength=130, command=partial(self.question_results, item))
            self.option_button.grid(row=item // 2, column=item % 2, padx=5, pady=5)

            self.option_button_ref.append(self.option_button)

        # list for buttons (frame | text | bg | command | width | row | column)
        control_button_list = [
            [self.quiz_frame, "Next Question", "#0057D8", lambda: self.new_question(all_questions), 21, 5],
            [self.quiz_frame, "Stats", "#333333", self.to_stats, 21, 6],
            [self.quiz_frame, "End", "#990000", self.close_play, 21, 7]
        ]

        # create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2], command=item[3], font=("Arial", 16, "bold"),
                                         fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        # retrieve next, stats and end button so that they can be configured
        self.next_button = control_ref_list[0]
        self.stats_button = control_ref_list[1]
        self.end_game_button = control_ref_list[2]

        self.stats_button.config(state=DISABLED)

        # Once interface has been created, invoke new question function for first question
        self.new_question(all_questions)


    def new_question(self, all_questions):
        """ Makes a question and asks the user. puts options into the buttons. """

        # retrieve number of questions answered, add one to it and configure heading
        questions_attempted = self.questions_attempted.get()
        questions_attempted += 1
        self.questions_attempted.set(questions_attempted)

        questions_wanted = self.questions_wanted.get()

        # get question and options
        self.question_and_answer_list = get_question_answer(all_questions)

        # update heading and score to beat labels. "Hide" results label
        self.target_label.config(text=f"Question {questions_attempted} out of {questions_wanted}")
        self.question_label.config(text=f"What is the practical translation for\n{self.question_and_answer_list[0]}?")
        self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

        # configure buttons using background colours from list
        # enable option buttons (disabled at the end of the last round)
        button_colour_list = ["#C9A0DC", "#BDF6FE", "#98FB98", "#FFEE8C"]
        for count, item in enumerate(self.option_button_ref):
            item.config(text=self.question_and_answer_list[2+count], bg=button_colour_list[count], state=NORMAL)
        self.next_button.config(state=DISABLED)


    def question_results(self, user_choice):
        """
        Retrieves which button was pushed, retrieves correct answer
        and then compares it with user's, updates results and adds
        to stats list.
        """
        # get user answer based on button press
        user_selection = self.option_button_ref[user_choice].cget('text')

        # get correct answer
        correct_answer = self.question_and_answer_list[1]

        # correct answer given
        if user_selection == correct_answer:
            result_text = f"Correct! {user_selection} was the correct translation."
            result_bg = "#82B366"
            right_answers = self.questions_correct.get()
            right_answers += 1
            self.questions_correct.set(right_answers)

        # incorrect answer given
        else:
            result_text = f"Oops! The correct answer is {correct_answer}, but you put {user_selection}."
            result_bg = "#F8CECC"

        self.results_label.config(text=result_text, bg=result_bg)

        # enable stats and next buttons, disable option buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)
        for item in self.option_button_ref:
            item.config(state=DISABLED)

        # check to see if the game is over
        questions_attempted = self.questions_attempted.get()
        questions_wanted = self.questions_wanted.get()
        if questions_attempted == questions_wanted:
            self.next_button.config(state=DISABLED, text="Quiz Complete")
            self.end_game_button.config(text="Try Again", bg="#006600")


    def to_stats(self):
        """
        Retrieves everything we need to display the game / round statistics
        """
        # IMPORTANT: retrieve number of questions correct
        # as a number (rather than the 'self' container)
        questions_wanted = self.questions_wanted.get()
        questions_attempted = self.questions_attempted.get()
        questions_correct = self.questions_correct.get()

        stats_bundle = [questions_wanted, questions_attempted, questions_correct]

        Stats(self, stats_bundle)


    def close_play(self):
        # reshow root (choose rounds) and end current game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


class Stats:

    def __init__(self, partner, all_stats_info):

        # disable buttons to prevent program crashing
        partner.end_game_button.config(state=DISABLED)
        partner.stats_button.config(state=DISABLED)

        # extract information from master list
        questions_wanted = all_stats_info[0]
        questions_attempted = all_stats_info[1]
        questions_correct = all_stats_info[2]

        # setup dialogue box
        self.stats_box = Toplevel()

        # disable stats button
        partner.stats_button.config(state=DISABLED)

        # if users press the cross at the top, closes stats and enables stats button.
        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

        # frame
        self.stats_frame = Frame(self.stats_box, width=350)
        self.stats_frame.grid()

        success_rate = questions_correct / questions_attempted * 100

        # Strings for stats labels
        progress_string = f"Progress: {questions_attempted} / {questions_wanted}"
        success_string = f"Success Rate: {questions_correct} / {questions_attempted} ({success_rate:.0f}%)"


        # custom comment text and formatting
        if questions_attempted == questions_correct:
            comment_string = ("Amazing! You have gotten every \n"
                              "question so far correct!")
            comment_colour = "#D5E8D4"

        elif questions_correct == 0:
            comment_string = ("Oops - You haven't gotten any \n"
                              "questions right! You might want \n"
                              "to do some revision.")
            comment_colour = "#F8CECC"

        else:
            comment_string = ""
            comment_colour = "#F0F0F0"

        heading_font = ("Arial", 16, "bold")
        normal_font = ("Arial", 14)
        comment_font = ("Arial", 13)

        # label list (text | font | 'Sticky')
        all_stats_strings = [
            ["Statistics", heading_font, ""],
            [progress_string, normal_font, "W"],
            [success_string, normal_font, "W"],
            [comment_string, comment_font, "W"],
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1], anchor="w",
                                     justify="left", padx=30, pady=5)
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append (self.stats_label)

        # configure comment label background (for all won / all lost)
        stats_comment_label = stats_label_ref_list[3]
        stats_comment_label.config(bg=comment_colour)

        self.dismiss_button = Button(self.stats_frame, font=("Arial", 16, "bold"), text="Dismiss",
                                     bg="#333333", fg="#FFFFFF", width=20, command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=8, padx=10, pady=10)


    def close_stats(self, partner):

        """Closes stats dialogue box and enables stats button."""
        # make buttons normal
        partner.end_game_button.config(state=NORMAL)
        partner.stats_button.config(state=NORMAL)

        self.stats_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Aikido Quiz")
    StartQuiz()
    root.mainloop()
















