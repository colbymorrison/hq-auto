import unittest
import search
import run

class SearchTest(unittest.TestCase):
    def setUp(self):
        ans0 = search.Answer("Test ans0")
        ans0.count = 2
        ans0.results = 0

        ans1 = search.Answer("Test ans1")
        ans1.count = 0
        ans0.results = 2

        ans2 = search.Answer("Test ans2")
        ans2.count = 1
        ans2.results = 3

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