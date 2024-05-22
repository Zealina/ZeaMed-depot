#!/usr/bin/env python3
"""Export the storage engine"""

from models.engine.sql_storage import SQLStorage

if 1 + 1 == 2:
    storage = SQLStorage()
    storage.reload()
