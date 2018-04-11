import search
import time
import os
import sys
import csv
import pandas as pd
import re


def statistics(arg):
    df = pd.read_csv("../log.csv")
    total = df.shape[0]
    percent = 100 * df[" SCORE"].value_counts(normalize=True)[1]
    print("Questions attempted: {} \nPercent correct: {}".format(total, round(percent, 2)))

    if arg == "-sv":
        print(df)


def document(q_as, most_likely, time_taken, correct):
    answers = q_as[1]
    chosen = answers.index(most_likely)

    if answers[correct] == most_likely:
        score = 1
    else:
        score = 0

    csv_dict = {'ques': q_as[0], 'ans0': answers[0].ans_str, 'ans1': answers[1].ans_str, 'ans2': answers[2].ans_str,
                'chosen': chosen, 'correct': correct, 'score': score, 'time': time_taken}

    with open("/Users/Colby/Code/Python/hq-auto/log.csv".format(os.getcwd()), 'a') as csvfile:
        fieldnames = ['ques', 'ans0', 'ans1', 'ans2', 'chosen', 'correct', 'score', 'time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(csv_dict)

    print("Logged")


def execute(mode):
    before = time.time()

    q_as, most_likely = search.search_and_rank(mode)

    if isinstance(most_likely, str):
        print(most_likely)
    else:
        print("Most likely answer: {}\n".format(most_likely.ans_str))

    os.system('./delete.sh')
    after = time.time()

    time_taken = round(after - before, 2)

    print("Time: {} s".format(time_taken))

    correct = int(input("What was the correct answer? "))

    while not(correct == 0 or correct == 1 or correct == 2):
        correct = input("Input 0, 1, or 2")

    document(q_as, most_likely, time_taken, correct)

    print('-'*50)


def run_game():
    path = "/Users/Colby/Code/Python/hq-auto/resources/auto-shot.png"
    try:
        while True:
            print("Waiting for screenshot...\n")
            while not os.path.exists(path):
                time.sleep(1)

            if os.path.isfile(path):
                execute(path)
    except KeyboardInterrupt:
        print("\nGoodbye!")


def main():
    arg1 = sys.argv[1]

    if arg1 == '-s' or arg1 == '-sv':
        statistics(arg1)
    else:
        print("Script has started \n")
        if arg1 == '-g':
            run_game()
        elif arg1 == '-l':
            execute(mode='l')
        else:
            execute("/Users/Colby/Code/Python/hq-auto/resources/auto-shot.png")


if __name__ == "__main__":
    main()
