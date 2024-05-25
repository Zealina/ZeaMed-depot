#!/usr/bin/env python3
"""
Test Script for Question and SQLStorage classes
"""

from models.question import Question
from models.engine.sql_storage import SQLStorage
from datetime import datetime

def test_question_class():
    print("Testing Question Class...")

    # Test initialization
    question_text = "What is the capital of France?"
    answer_text = "Paris"
    options = ["Berlin", "Madrid", "Paris", "Rome"]
    question = Question(question=question_text, answer=answer_text, options=options)

    print(f"Question initialized: {question}")

    # Test properties
    print(f"Question ID: {question.id}")
    print(f"Question text: {question.question}")
    print(f"Answer: {question.answer}")
    print(f"Options: {question.options}")
    print(f"Verified: {question.verified}")
    print(f"Posting: {question.posting}")
    print(f"PQ: {question.pq}")
    print(f"Explanation: {question.explanation}")
    print(f"Topic: {question.topic}")
    print(f"Created at: {question.created_at}")
    print(f"Updated at: {question.updated_at}")

    # Test to_dict
    question_dict = question.to_dict()
    print(f"Question to_dict: {question_dict}")

    # Test update
    question.update(question="What is the largest planet?", answer="Jupiter", options=["Earth", "Jupiter", "Mars", "Venus"])
    print(f"Updated Question: {question}")

def test_sql_storage_class():
    print("Testing SQLStorage Class...")

    # Initialize storage
    storage = SQLStorage()
    storage.reload()

    # Create a new question
    question_text = "What is the capital of Germany?"
    answer_text = "Berlin"
    options = ["Berlin", "Madrid", "Paris", "Rome"]
    new_question = Question(question=question_text, answer=answer_text, options=options)

    # Add and save the new question
    storage.new(new_question)
    storage.save()
    print(f"New Question added and saved: {new_question}")

    # Retrieve all questions
    all_questions = storage.all()
    print("All Questions:", all_questions)

    # Retrieve a question by ID
    retrieved_question = storage.get(new_question.id)
    print(f"Retrieved Question by ID: {retrieved_question}")

    # Count questions
    question_count = storage.count()
    print(f"Number of Questions: {question_count}")

    # Update a question
    retrieved_question.update(question="What is the largest continent?", answer="Asia", options=["Africa", "Asia", "Europe", "North America"])
    storage.save()
    print(f"Updated Question: {retrieved_question}")

    # Delete a question
    storage.delete(retrieved_question)
    storage.save()
    print(f"Deleted Question: {retrieved_question}")

    # Count questions after deletion
    question_count_after_deletion = storage.count()
    print(f"Number of Questions after deletion: {question_count_after_deletion}")

    # Close storage session
    storage.close()

if __name__ == "__main__":
    test_question_class()
    test_sql_storage_class()
