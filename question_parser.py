import re
from models.question import Question

def parse_question_file(file_path):
    questions = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Extract global metadata
    global_metadata = {}
    question_start_index = 0
    for i, line in enumerate(lines):
        if line.strip() == '':
            continue
        if line.startswith('Q:'):
            question_start_index = i
            break
        key, value = line.split(':', 1)
        global_metadata[key.strip().lower()] = value.strip()
    
    raw_questions = ''.join(lines[question_start_index:]).split('\nQ:')

    for raw_question in raw_questions:
        if raw_question.strip():
            q_data = {
                'question': None, 
                'answer': None, 
                'options': [], 
                'posting': global_metadata.get('posting'), 
                'topic': global_metadata.get('topic'), 
                'pq': global_metadata.get('pq', 'True').lower() == 'true', 
                'explanation': None, 
                'verified': False
            }

            # Clean up raw_question text by removing leading Q:
            if raw_question.startswith('Q:'):
                raw_question = raw_question[2:].strip()

            # Extract question data using regex
            question_match = re.search(r'^(.+?)\n', raw_question)
            if question_match:
                q_data['question'] = question_match.group(1).strip()
            answer_match = re.search(r'Answer:\s*(.+)', raw_question)
            if answer_match:
                q_data['answer'] = answer_match.group(1).strip()
            options_match = re.search(r'Options:\s*\[(.*?)\]', raw_question)
            if options_match:
                q_data['options'] = [opt.strip() for opt in options_match.group(1).split(',')]
            explanation_match = re.search(r'Explanation:\s*(.+)', raw_question)
            if explanation_match:
                q_data['explanation'] = explanation_match.group(1).strip()
            
            question = Question(**q_data)
            questions.append(question)
    
    return questions
