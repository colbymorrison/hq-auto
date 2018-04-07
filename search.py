from PIL import Image
from googleapiclient.discovery import build
import pytesseract
import os
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


def number_results(res, answer):
    search_inf = res['searchInformation']
    return {'ans': answer, 'res':  search_inf['totalResults']}


def word_matches(res, answer):
    items = res['items']
    count = 0
    for i in items:
        for value in i.values():
            if isinstance(value, str):
                count += value.lower().count(answer.lower())

    return {'ans': answer, 'count': count}


def search_answer(q_as, num, opt):
    question = q_as['ques']
    answer = q_as['ans{}'.format(num)]
    if opt == 0:
        res = google_search("{} {}".format(question, answer))
        return number_results(res, answer)
    else:
        res = google_search(question)
        return word_matches(res, answer)


def search(file):
    q_as = img_to_text(file)
    results = []

    print("Question --------------> {} \n".format(q_as['ques']))

    for i in range(0, 3):
        results.append(search_answer(q_as, i, 1))

    results = sorted(results, key=lambda d: d['count'], reverse=True)

    print("Most Likely Answer ----> {} with {} matches\n".format(results[0]['ans'], results[0]['count']))

    for dct in results[1:]:
        print("Answer ----------------> {} with {} matches\n ".format(dct['ans'], dct['count']))

    os.system('./callpy.sh')


def main():
    path = "resources/auto-shot.png"

    while not os.path.exists(path):
        time.sleep(1)

    if os.path.isfile(path):
        search(path)


if __name__ == "__main__":
    main()
