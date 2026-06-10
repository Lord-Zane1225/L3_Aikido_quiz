import csv
import random

# retrieve colours from csv file and put them in a list
file = open("Aikido Quiz Database.csv", "r")
all_questions = list(csv.reader(file, delimiter=","))
file.close()

# remove the first row
all_questions.pop(0)

answer_options = []

# loop until we have four options
while len(answer_options) < 4:
    potential_option = random.choice(all_questions)
    answer_options.append(potential_option)

print(answer_options)

