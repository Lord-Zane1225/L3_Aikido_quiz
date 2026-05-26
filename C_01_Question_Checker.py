# function goes here

def question_checker(amt_requested, max_questions):
    error = f"Please enter an integer more than 0 and less than {max_questions}."
    if amt_requested == "" or amt_requested < 0 or amt_requested > max_questions:
        print(error)
        return "fail"
    else:
        try:
            amt_requested = int(amt_requested)
            return amt_requested
        except ValueError:
            print(error)
            return "fail"

# main routine starts here

amt_questions = question_checker(input("Please enter the amount of questions you wish to answer (max 40)"), 40)
print(amt_questions)
