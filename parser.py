#!/usr/bin/env python3
"""Parsing algorithm implementation"""

import re
from models.question import Question

with open(file_name, "r") as fp:
    line = read_line
    while line:
        if line.startswith("Q: "):
            line = line.replace(""
