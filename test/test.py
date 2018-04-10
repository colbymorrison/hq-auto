import unittest
import search
import run


class SearchTest(unittest.TestCase):
    def setUp(self):
        ans0 = search.Answer("Feather")
        ans0.count = 8
        ans0.results = 25800

        ans1 = search.Answer("Noodle soup")
        ans1.count = 0
        ans0.results = 14100

        ans2 = search.Answer("Duck")
        ans2.count = 0
        ans2.results = 27100

        Feather, 8, 25800.
        Noodle
        soup, 0, 14100.
        Duck, 0, 27100

        self.answers = [ans0, ans1, ans2]

    # def test_rank(self):
    #     most_likely = search.rank(self.answers)
    #     assert(isinstance(most_likely, str))
    #
    #     self.answers[0].results = 4
    #
    #     most_likely = search.rank(self.answers)
    #     assert(most_likely.ans_str == "Test ans0")

    def test_document(self):
        most_likley = self.answers[0]
        question = "Test question"
        q_as = [question, self.answers]

        run.document(q_as, most_likley, time_taken="2.5s", correct=0)


if __name__ == "__main__":
    unittest.main()