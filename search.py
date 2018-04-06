from PIL import Image
from googleapiclient.discovery import build
import pytesseract
import pprint





def img_to_text(file):
    tess = pytesseract.image_to_string(Image.open(file))
    ques, ans1, ans2, ans3 = "", "", "", ""
    ln = 0

    for i in tess.split('\n'):
        if i.strip():
            ques += i
            ln = ln + 1
            if i.endswith("?"):
                ans1 = tess.splitlines()[ln + 2]
                ans2 = tess.splitlines()[ln + 4]
                ans3 = tess.splitlines()[ln + 6]
                break

    q_as = {'ques': ques, 'ans1': ans1, 'ans2': ans2, 'ans3': ans3}
    return q_as


def google_search(string):
    service = build("customsearch", "v1",
                    developerKey="AIzaSyCVsjb-Ar3mE-oZRiTYjsG4qLm85NxLkws")
    res = service.cse().list(q=string, cx="004635228232604600486:dehcqnd7kkq", num=10).execute()
    res = res['items']
    for result in res:
        pprint.pprint(result)


def search(file):
    q_as = img_to_text(file)
    google_search(q_as['ques'])



def main():
    serach_google("hello")


if __name__ == "__main__":
    main()
