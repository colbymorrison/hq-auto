# Inspired by hackernoon.com/i-hacked-hq-trivia-but-heres-how-they-can-stop-me-68750ed16365

from PIL import Image
from googleapiclient.discovery import build
import pytesseract
import os
import webbrowser
import inflect


service = build("customsearch", "v1", developerKey="AIzaSyCVsjb-Ar3mE-oZRiTYjsG4qLm85NxLkws")


class Answer:
    def __init__(self, answer):
        self.ans_str = answer
        self.count = 0
        self.results = 0

    def set_count(self, res):
            items = res['items']
            count = 0
            for i in items:
                count += i['snippet'].lower().count(self.ans_str.lower())

            self.count = count

    def set_results(self, question):
        search_str = "{} {}".format(question, self.ans_str)
        res = service.cse().list(q=search_str, cx="004635228232604600486:dehcqnd7kkq", num=10).execute()
        search_inf = res['searchInformation']
        self.results = int(search_inf['totalResults'])

    def print_out(self):
        print("{}, {} , {}. ".format(self.ans_str, self.count, self.results))


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
            ans0 = Answer(lines[ln])
            ans1 = Answer(lines[ln+1])
            ans2 = Answer(lines[ln+2])
            break

    q_as = [ques, [ans0, ans1, ans2]]
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


def rank_helper(answers):
    found, i = 0, 0
    for answer in answers:
        if answer.count == 0:
            i += 1
        else:
            found = answers.index(answer)

    if i == 2:
        return True, found
    else:
        return False, found


def rank(answers):
    # From dictionary of answers sored by count and number of results picks the most likeley answer to the question
    count_sort = sorted(answers, key=lambda a: a.count, reverse=True)
    results_sort = sorted(answers, key=lambda a: a.results, reverse=True)

    boole, found = rank_helper(answers)

    if count_sort[0] == results_sort[0]:
        most_likely = count_sort[0]
    elif count_sort[0].count == count_sort[1].count == count_sort[2].count:
        most_likely = results_sort[0]
    elif count_sort[0].results == count_sort[1].results == count_sort[2].results:
            most_likely = count_sort[0]
    elif boole:
        most_likely = answers[found]
    else:
        most_likely = "Conflicted: {} had highest count but {} had most results"\
            .format(count_sort[0].ans_str, results_sort[0].ans_str)

    return most_likely


def search_from_photo(path):
    q_as = img_to_text(path)

    question_raw = q_as[0]
    answers = q_as[1]

    print("Question --------------> {} \n".format(question_raw))
    webbrowser.open("https://www.google.com/search?q={}".format(question_raw))

    i = 0
    for answer in answers:
        print("Answer {}: -------------> {}\n".format(i, answer.ans_str))
        i += 1

    res, cor_ques = google_search_question(question_raw)
    q_as[0] = cor_ques

    for answer in answers:
        answer.set_count(res)
        answer.set_results(cor_ques)

    most_likely = rank(answers)

    return q_as, most_likely