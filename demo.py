#!/usr/bin/env python3

# demo.py

from models.base_model import BaseModel
from models.user import User
from models.engine.db_storage import Storage

# Initialize storage
storage = Storage()
storage.reload()

# Create a user instance
user_data = {
    "email": "example@example.com",
    "password": "password123",
    "firstname": "John",
    "lastname": "Doe",
    "username": "johndoe"
}
new_user = User(**user_data)

# Add the user to the database
storage.add(new_user)

# Print out the added user
print("\nAdded User:")
print(new_user)

# Retrieve the user by ID
retrieved_user = storage.get(User, new_user.id)

# Print out the retrieved user
print("\nRetrieved User:")
print(retrieved_user)

# Update the user's details
retrieved_user.firstname = "Jane"
storage.update(retrieved_user)

# Print out the updated user
print("\nUpdated User:")
print(storage.get(User, retrieved_user.id))

# Close the storage session
storage.close()
