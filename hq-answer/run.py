import search
import time
import os
import sys
import csv


def document(q_as, most_likely, time, correct):
    i = 0
    for key, value in q_as.items():
        if value == most_likely:
            break
        i += 1

    q_as.update({'pick': i - 1, 'time': time, 'correct': correct})

    with open("questions_answers.csv", 'a') as csvfile:
        fieldnames = ['ques', 'ans0', 'ans1', 'ans2', 'pick', 'time', 'correct']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(q_as)


def get_results(path):
    q_as, most_likely, best_count, best_results = search.search_from_photo(path)

    if most_likely == "CLASH":
        print("Conflicted: {} had highest count but {} had most results"
              .format(best_count['ans'], best_results['ans']))
    else:
        print("\nMost likely answer: {}\n".format(most_likely))

    os.system('./delete.sh')

    return q_as, most_likely


def execute(path):
    before = time.time()
    q_as, most_likely = get_results(path)
    after = time.time()

    time_taken = after - before

    print("Time: {} s\n\n".format(after - before))

    correct = input("Was I correct? (y/n)")

    while not(correct == "y" or correct == "n"):
        correct = input("Input y for correct, f for incorrect")

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
    path = "resources/shot-7.51.29 PM.png"

    if sys.argv[1] == 0:
        run_game(path)
    else:
        execute(path)


if __name__ == "__main__":
    main()
