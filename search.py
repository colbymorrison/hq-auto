from PIL import Image
from googleapiclient.discovery import build
import pytesseract
import os


def img_to_text(file):
    tess = pytesseract.image_to_string(Image.open(file))
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


def google_search(question, answer):
    search_str = "{} {}".format(question, answer)
    service = build("customsearch", "v1",
                    developerKey="AIzaSyCVsjb-Ar3mE-oZRiTYjsG4qLm85NxLkws")
    res = service.cse().list(q=search_str, cx="004635228232604600486:dehcqnd7kkq", num=1).execute()

    try:
        spell = res['spelling']
        corr_str = spell['correctedQuery']
        print(corr_str)
        resNew = service.cse().list(q=corr_str, cx="004635228232604600486:dehcqnd7kkq", num=1).execute()
        search = resNew['searchInformation']
    except KeyError:
        search = res['searchInformation']

    return {'ans': answer, 'res':  search['totalResults']}


def search_answer(q_as, num):
    answer = q_as['ans{}'.format(num)]
    return google_search(q_as['ques'], answer)


def search(file):
    q_as = img_to_text(file)
    results = []
    for i in range(0, 3):
        results.append(search_answer(q_as, i))

    best = max(results[0]['res'], results[1]['res'], results[2]['res'])

    for dct in results:
        if dct['res'] == best:
            print("{} with {} results\n\n".format(dct['ans'], dct['res']))
            results.remove(dct)

    for dct in results:
        print("{} with {} results".format(dct['ans'], dct['res']))


def main():
    search("resources/screenshot-5.png")
    #google_search("hi", "hi")
    #print(img_to_text("resources/screenshot-8.png"))

if __name__ == "__main__":
    main()
