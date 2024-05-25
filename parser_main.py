from question_parser import parse_question_file

questions = parse_question_file('pharmacology_questions.txt')

for question in questions:
    print(question.to_dict())
