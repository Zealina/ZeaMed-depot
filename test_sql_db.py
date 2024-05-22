#!/usr/bin/env python3
"""Test the sql database connection"""

from models.engine.sql_storage import SQLStorage
from sqlalchemy import text

storage = SQLStorage()


print(storage.connection)

with storage.connection as conn:
    result = conn.execute(text("SHOW TABLES"))
    print(result.all())
