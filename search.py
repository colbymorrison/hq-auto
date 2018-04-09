# Inspired by hackernoon.com/i-hacked-hq-trivia-but-heres-how-they-can-stop-me-68750ed16365

from PIL import Image
from googleapiclient.discovery import build
import pytesseract
import os
import webbrowser
import logging
import sys
import datetime
import time


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


def google_search(search_str):
    # Searches google for a string
    service = build("customsearch", "v1", developerKey="AIzaSyCVsjb-Ar3mE-oZRiTYjsG4qLm85NxLkws")
    res = service.cse().list(q=search_str, cx="004635228232604600486:dehcqnd7kkq", num=10).execute()

    try:
        spell = res['spelling']
        corr_str = spell['correctedQuery']
        res = service.cse().list(q=corr_str, cx="004635228232604600486:dehcqnd7kkq", num=10).execute()

    finally:
        return res


def results_dict(q_as, num):
    # Creates dictionary of answer, the number of times it appeared in the first 10 google results,
    # and the total number of google search results the question/answer combination returned
    question = q_as['ques']
    answer = q_as['ans{}'.format(num)]

    res = google_search("{} {}".format(question, answer))
    search_inf = res['searchInformation']

    res_b = google_search(question)
    items = res_b['items']
    count = 0
    for i in items:
        for value in i.values():
            if isinstance(value, str):
                count += value.lower().count(answer.lower())

    return {'ans': answer, 'results':  int(search_inf['totalResults']), 'count': count}


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

    print("Question --------------> {} \n".format(q_as['ques']))
    #webbrowser.open("https://www.google.com/search?q={}".format(q_as['ques']))

    for i in range(0, 3):
        results.append(results_dict(q_as, i))

    count_sort = sorted(results, key=lambda d: d['count'], reverse=True)
    results_sort = sorted(results, key=lambda d: d['results'], reverse=True)

    res = rank(count_sort, results_sort)

    print(count_sort)
    print(results_sort)

    print("\n Most likely answer: {}".format(res['ans']))


    # i = 0
    #
    # print("Answers by count: \n")
    # for dct in count_sort:
    #     print("{}: {} --------> with {} matches\n".
    #           format(i, dct['ans'], dct['count']))
    #     i += 1
    #
    # i = 0
    # print("Answers by results: \n")
    # for dct in results_sort:
    #     print("{}: {} --------> with {} matches \n".
    #           format(i, dct['ans'], dct['count']))
    #
    # os.system('./delete.sh')


def main():
    path = "resources/shot-7.51.21 PM.png"

    while not os.path.exists(path):
        time.sleep(1)

    if os.path.isfile(path):
        before = time.time()
        search(path)
        after = time.time()

        print("Time: {}".format(after-before))


if __name__ == "__main__":
    main()
