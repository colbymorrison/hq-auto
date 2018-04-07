from PIL import Image
from googleapiclient.discovery import build
import pytesseract
import os
import logging
import sys
import time


def img_to_text(path):
    tess = pytesseract.image_to_string(Image.open(path))
    ques, ans0, ans1, ans2 = "", "", "", ""
    ln = 0

    tess = os.linesep.join([s for s in tess.splitlines() if s])
    tess = tess.replace('"', ' ')
    tess = tess.replace('\'', ' ')

    for i in tess.splitlines():
        if not i.strip(): continue
        if not i[0:1].isalpha():
            ln = ln + 1
            continue
        ques += i
        ln = ln + 1
        if i.endswith("?"):
            ans0 = tess.splitlines()[ln]
            ans1 = tess.splitlines()[ln+1]
            ans2 = tess.splitlines()[ln+2]
            break

    ques = ques.replace("\"","")
    q_as = {'ques': ques, 'ans0': ans0, 'ans1': ans1, 'ans2': ans2}
    return q_as


def google_search(search_str):
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


def search(file):
    q_as = img_to_text(file)
    results = []

    print("Question --------------> {} \n".format(q_as['ques']))

    for i in range(0, 3):
        results.append(results_dict(q_as, i))

    count_sort = sorted(results, key=lambda d: d['count'], reverse=True)
    results_sort = sorted(results, key=lambda d: d['results'], reverse=True)

    print(results_sort)

    if count_sort[0] == results_sort[0]:
        most_likely = count_sort[0]
    else:
        most_likely = results_sort[0]

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
