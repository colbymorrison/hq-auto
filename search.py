from PIL import Image
from googleapiclient.discovery import build
import pytesseract
import os
import logging
import sys
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
    service = build("customsearch", "v1",
                    developerKey="AIzaSyCVsjb-Ar3mE-oZRiTYjsG4qLm85NxLkws")
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

    return {'ans': answer, 'results':  search_inf['totalResults'], 'count': count}


def rank(count_sort, results_sort):
    # From dictionary of answers sored by count and number of results picks the most likeley answer to the question
    if count_sort[0] == results_sort[0]:
        most_likely = count_sort[0]
    else:
        most_likely = results_sort[0]

    return most_likely


def search(file):
    q_as = img_to_text(file)
    results = []

    print("Question --------------> {} \n".format(q_as['ques']))

    for i in range(0, 3):
        results.append(results_dict(q_as, i))

    count_sort = sorted(results, key=lambda d: d['count'], reverse=True)
    results_sort = sorted(results, key=lambda d: d['results'], reverse=True)

    most_likely = rank(count_sort, results_sort)

    print("Most Likely Answer ----> {} with {} matches and {} results\n".
          format(most_likely['ans'], most_likely['count'], most_likely['results']))

    for dct in results[1:]:
        print("Answer ----------------> {} with {} matches and {} results\n "
              .format(dct['ans'], dct['count'], dct['results']))

    #os.system('./delete.sh')


def main():
    path = "resources/screenshot-5.png"

    while not os.path.exists(path):
        time.sleep(1)

    if os.path.isfile(path):
        search(path)


if __name__ == "__main__":
    main()
