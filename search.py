# Inspired by hackernoon.com/i-hacked-hq-trivia-but-heres-how-they-can-stop-me-68750ed16365

from PIL import Image
from googleapiclient.discovery import build
import pytesseract
import os
import webbrowser
import time
import sys

service = build("customsearch", "v1", developerKey="AIzaSyCVsjb-Ar3mE-oZRiTYjsG4qLm85NxLkws")

def img_to_text(path):
    # Extracts text from an image 
    tess = pytesseract.image_to_string(Image.open(path))
    ques, ans0, ans1, ans2 = "", "", "", ""
    ln = 0
    lines = tess.splitlines()

    # remove blank lines and quotes
    tess = os.linesep.join([s for s in lines if s])
    tess = tess.replace('"', ' ')
    tess = tess.replace('\'', ' ')

    lines = tess.splitlines()

    for i in lines:
        if not i.strip(): continue
        if not i[0:1].isalpha():
            ln = ln + 1
            continue
        ques += i
        ln = ln + 1
        if i.endswith("?"):
            ans0 = lines[ln]
            ans1 = lines[ln+1]
            ans2 = lines[ln+2]
            break

    # Return dictionary of question and answers
    q_as = {'ques': ques, 'ans0': ans0, 'ans1': ans1, 'ans2': ans2}
    return q_as


def google_search_question(question):
    corr_str = question
    res = service.cse().list(q=question, cx="004635228232604600486:dehcqnd7kkq", num=10).execute()

    try:
        spell = res['spelling']
        corr_str = spell['correctedQuery']
        res = service.cse().list(q=corr_str, cx="004635228232604600486:dehcqnd7kkq", num=10).execute()

    finally:
        return res, corr_str


def answer_count(res, answer):
    items = res['items']
    count = 0
    for i in items:
        count += i['snippet'].lower().count(answer.lower())

    return {'count': count}


def answer_results(question, answer):
    # Creates dictionary of answer, the number of times it appeared in the first 10 google results,
    # and the total number of google search results the question/answer combination returned
    #print(("{} {}".format(question, answer)))
    search_str = "{} {}".format(question, answer)
    res = service.cse().list(q=search_str, cx="004635228232604600486:dehcqnd7kkq", num=10).execute()
    search_inf = res['searchInformation']

    return {'ans': answer, 'results':  int(search_inf['totalResults'])}


def rank(count_sort, results_sort):
    # From dictionary of answers sored by count and number of results picks the most likeley answer to the question
    if count_sort[0] == results_sort[0]:
        return count_sort[0]
    elif count_sort[0]["count"] == count_sort[1]["count"] == count_sort[2]["count"]:
            return results_sort[0]
    elif count_sort[0]["results"] == count_sort[1]["results"] == count_sort[2]["results"]:
            return count_sort[0]
    else:
        return {'ans': "CLASH"}


def search(file):
    q_as = img_to_text(file)
    results = []

    question_raw = q_as['ques']

    print("Question --------------> {} \n".format(question_raw))
    #webbrowser.open("https://www.google.com/search?q={}".format(question_raw))

    res, cor_ques = google_search_question(question_raw)

    for i in range(0, 3):
        answer = q_as['ans{}'.format(i)]
        results_dict = answer_results(cor_ques, answer)
        results_dict.update(answer_count(res, answer))
        results.append(results_dict)

    count_sort = sorted(results, key=lambda d: d['count'], reverse=True)
    results_sort = sorted(results, key=lambda d: d['results'], reverse=True)

    most_likely = rank(count_sort, results_sort)['ans']

    if most_likely == "CLASH":
        print("Conflicted: {} had highest count but {} had most results"
              .format(count_sort[0]['ans'], results_sort[0]['ans']))
    else:
        print("\n Most likely answer: {}\n".format(most_likely))

    os.system('./delete.sh')


def execute(path):
    before = time.time()
    search(path)
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
