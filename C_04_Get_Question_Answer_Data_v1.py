import csv
import random

# retrieve colours from csv file and put them in a list
file = open("quiz/Aikido Quiz Database.csv", "r")
all_questions = list(csv.reader(file, delimiter=","))
file.close()

# remove the first row
all_questions.pop(0)

answer_options = []
colour_scores = []

# pick a question
quiz_question_chosen = random.choice(all_questions)

# loop until we have four colours with different scores
while len(answer_options) < 4:
    potential_colour = random.choice(all_questions)

    # get the score and check it's not a duplicate
    if potential_colour[1] not in colour_scores:
        answer_options.append(potential_colour)
        colour_scores.append(potential_colour[1])

print(answer_options)
print(colour_scores)

# find target score (median)

# change scores to integers
int_scores = [int(x) for x in colour_scores]
print("scores unsorted", int_scores)
int_scores.sort()
print("scores sorted", int_scores)

median = (int_scores[1] + int_scores[2]) / 2
median = round_ans(median)
print("median", median)


