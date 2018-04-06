from PIL import Image
from googleapiclient.discovery import build
import pytesseract


def img_to_text(file):
    tess = pytesseract.image_to_string(Image.open(file))
    ques, ans0, ans1, ans2 = "", "", "", ""
    ln = 0

    for i in tess.split('\n'):
        if not i.strip(): continue
        if not i[0:1].isalpha():
            ln = ln + 1
            continue
        ques += i
        ln = ln + 1
        if i.endswith("?"):
            ans0 = tess.splitlines()[ln + 2]
            ans1 = tess.splitlines()[ln + 4]
            ans2 = tess.splitlines()[ln + 6]
            break

    ques = ques.replace("\"","")
    q_as = {'ques': ques, 'ans0': ans0, 'ans1': ans1, 'ans2': ans2}
    return q_as


def google_search(question, answer):
    search_str = "{} \"{}\"".format(question, answer)
    service = build("customsearch", "v1",
                    developerKey="AIzaSyCVsjb-Ar3mE-oZRiTYjsG4qLm85NxLkws")
    res = service.cse().list(q=search_str, cx="004635228232604600486:dehcqnd7kkq", num=1).execute()
    res = res['searchInformation']
    return res['totalResults']


def search_answer(q_as, num):
    answer = q_as['ans{}'.format(num)]
    results = google_search(q_as['ques'], answer)
    print("{}: {}\n".format(answer, results))


def search(file):
    q_as = img_to_text(file)
    for i in range(0, 3):
        search_answer(q_as, i)


def main():
    search("resources/screenshot-1.png")


if __name__ == "__main__":
    main()
