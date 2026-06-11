import csv
import random

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
    answer_options.append(potential_option[2])

# add correct answer to a random place in the answer options
answer_options.insert(random.randint(0, 4), quiz_question_chosen[2])

print(quiz_question_chosen)
print()
print(answer_options)

