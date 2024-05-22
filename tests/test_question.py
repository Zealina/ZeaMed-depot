import unittest
from models.question import Question

class TestQuestion(unittest.TestCase):

    def test_question_initialization(self):
        q = Question(question="What is the capital of France?")
        self.assertEqual(q.question, "What is the capital of France?")
        self.assertEqual(q.answer, None)
        self.assertEqual(q.options, [True, False])
        self.assertEqual(q.verified, False)
        self.assertEqual(q.pq, True)

    def test_question_setter(self):
        q = Question(question="What is the capital of France?")
        q.question = "What is 2+2?"
        self.assertEqual(q.question, "What is 2+2?")
        with self.assertRaises(ValueError):
            q.question = None

    def test_answer_setter(self):
        q = Question(question="What is 2+2?", options=[2, 3, 4])
        q.answer = 4
        self.assertEqual(q.answer, 4)
        with self.assertRaises(ValueError):
            q.answer = 5

    def test_to_dict(self):
        q = Question(question="What is the capital of France?")
        q_dict = q.to_dict()
        self.assertEqual(q_dict['question'], "What is the capital of France?")

if __name__ == '__main__':
    unittest.main()
