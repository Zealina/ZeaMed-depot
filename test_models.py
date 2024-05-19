#!/usr/bin/env python3
"""Test the questions model"""

from models.question import Question

text = "What is the name of the longest bone in the human body?"
answer = "Femur"
posting = "Extremities"

q = Question(text, answer, posting=posting)

print(q.to_dict())

print()

print(q)
