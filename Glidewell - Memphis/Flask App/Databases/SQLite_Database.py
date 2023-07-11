###############################################################################################
####################### Code to create fake database in SQLite for testing purposes ###########

import os
import random
from datetime import date
from flask import Flask, render_template, request, redirect, session

## Notes: These operations constitute the main CRUD operations that the user will have access to while using the application
# from manage_user import ManageUser, retrieve_user, insert_user, update_user, delete_user
import sqlite3
from faker import Faker
from passlib.hash import sha256_crypt

departments = [
    "Engineering and Technology",
    "Human Resources",
    "Accounting",
    "Marketing",
]

# Create faker instance
fake = Faker()

users = []
for _ in range(500):
    tech_id = fake.random_int(min=100000, max=999999)
    first_name = fake.first_name()
    last_name = fake.last_name()
    department = random.choice(departments)
    username = f"{first_name.lower()}.{last_name.lower()}"
    password = fake.password(length=6)
    hashed_password = sha256_crypt.hash(password)
    users.append(
        (
            tech_id,
            first_name,
            last_name,
            department,
            username,
            password,
            hashed_password,
        )
    )

## Note: This line of the code is important as it establishes the connection to the database
conn = sqlite3.connect("user.db")
c = conn.cursor()


## Note: The INTEGER Datatype has the following size specifications -2147483648 to 2147483647 (Signed)
c.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          tech_id INTEGER,
          first_name TEXT,
          last_name TEXT,
          department TEXT,
          username TEXT,
          password TEXT,
          hashed_password TEXT
          )
          """
)

c.executemany(
    "INSERT INTO users (tech_id, first_name, last_name, department, username, password, hashed_password) VALUES (?, ?, ?, ?, ?, ?, ?)",
    users,
)
conn.commit()
conn.close()

## Note: Line of code added to find the database link.
## Will make changes to the database using the GUI, in this case DB Browser for SQLite

database_filename = "users.db"

current_directory = os.getcwd()
database_path = os.path.join(current_directory, database_filename)

print("Database path: ", database_path)

###############################################################################################
