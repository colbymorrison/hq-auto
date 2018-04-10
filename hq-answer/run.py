import search
import time
import os
import sys
import csv


def document(q_as, most_likely, time_taken, correct):
    answers = q_as[1]
    chosen = answers.index(most_likely)

    if answers[correct] == most_likely:
        score = 1
    else:
        score = 0

    csv_dict = {'ques': q_as[0], 'ans0': answers[0].ans_str, 'ans1': answers[1].ans_str, 'ans2': answers[2].ans_str,
                'chosen': chosen, 'correct': correct, 'score': score, 'time': time_taken}

    with open("../questions_answers.csv", 'a') as csvfile:
        fieldnames = ['ques', 'ans0', 'ans1', 'ans2', 'chosen', 'correct', 'score', 'time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(csv_dict)


def execute(path):
    before = time.time()
    q_as, most_likely = search.search_from_photo(path)

    if isinstance(most_likely, str):
        print(most_likely)
    else:
        print("Most likely answer: {}\n".format(most_likely.ans_str))

    os.system('./delete.sh')
    after = time.time()

    time_taken = round(after - before, 2)

    print("Time: {} s".format(after - before))

    correct = int(input("What was the correct answer? (0, 1, 2)"))

    while not(correct == 0 or correct == 1 or correct == 2):
        correct = input("Input 0, 1, or 2")

    document(q_as, most_likely, time_taken, correct)


def run_game(path):
    try:
        while True:
            while not os.path.exists(path):
                time.sleep(1)

            if os.path.isfile(path):
                execute(path)
    except KeyboardInterrupt:
        print("\nGoodbye!")


def main():
    print("Script has started \n")
    path = "../resources/shot-7.51.25 PM.png"

    if sys.argv[1] == 0:
        run_game(path)
    else:
        execute(path)


if __name__ == "__main__":
    main()
