# function goes here

def question_checker(amt_requested, max_questions):
    # error message
    error = f"Please enter an integer more than 0 and less than {max_questions + 1}."

    # error checker
    try:
        # is integer?
        amt_requested = int(amt_requested)
        # make sure user response is within parameters
        if amt_requested < 0 or amt_requested > max_questions:
            # fail
            print(error)
            return "fail"
        else:
            # success
            return amt_requested

    except ValueError:
        # fail
        print(error)
        return "fail"


# main routine starts here

amt_questions = question_checker(input("Please enter the amount of questions you wish to answer (max 40)"), 40)
print(amt_questions)