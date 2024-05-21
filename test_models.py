#!/usr/bin/env python3
"""Test the questions model"""

from models.question import Question

parameters = {
              "answer":"Femur",
              "posting":"Extremities",
              "topic":"Osteology of Lower Extremitiies",
              "options": ["Femur", "Humerus", "Incus"]
              }
text = "What is the name of the longest bone in the human body?"

q = Question(text, **parameters)

print(q.to_dict())

print()

print(q)

q.update(options=["cat", "dog"])

print(q.to_dict())
