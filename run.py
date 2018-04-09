import time
import search
import os
import sys


def get_results(path):
    most_likely, best_count, best_results = search.search_from_photo(path)

    if most_likely == "CLASH":
        print("Conflicted: {} had highest count but {} had most results"
              .format(best_count['ans'], best_results['ans']))
    else:
        print("\n Most likely answer: {}\n".format(most_likely))

    os.system('./delete.sh')


def execute(path):
    before = time.time()
    get_results(path)
    after = time.time()

    print("Time: {} s\n\n".format(after - before))


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