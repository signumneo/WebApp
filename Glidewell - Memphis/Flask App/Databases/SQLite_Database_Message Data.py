import random
import string
import sqlite3  # Assuming you're using SQLite as the SQL database
import os

from faker import Faker

# Create a connection to the SQLite database
conn = sqlite3.connect("message.db")
cursor = conn.cursor()

# Create the table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS message_information (
        EType INTEGER,
        Id INTEGER,
        Fb INTEGER,
        P1 INTEGER,
        P2 TEXT,
        P3 TEXT,
        P4 TEXT,
        P5 TEXT,
        P6 TEXT,
        P7 TEXT,
        P8 TEXT,
        P9 TEXT,
        P10 TEXT,
        P11 INTEGER,
        P12 INTEGER,
        P13 INTEGER,
        P14 INTEGER,
        P15 INTEGER,
        P16 INTEGER,
        P17 INTEGER,
        P18 INTEGER,
        P19 INTEGER,
        P20 INTEGER
    )
"""
)

# Create an instance for the Faker class
fake = Faker()

# DeWax Tray ID options defined for the demo database
P3_val = ["S001", "S010", "S011", "S100", "S101", "S110", "S111"]
P9_val = ["S001", "S010", "S100", "S101", "S110", "S111"]

# Generate and insert fake user information
for _ in range(200):
    EType = 0
    Id = 0
    Fb = fake.random_int(min=100000000, max=999999999)
    P1 = fake.random_int(min=1000001, max=9999999)
    P2 = "".join(
        [
            str(random.randint(100, 999)),
            "".join(random.choices(string.ascii_letters, k=3)),
            str(random.randint(100, 999)),
            "".join(random.choices(string.ascii_letters, k=3)),
            str(random.randint(100, 999)),
        ]
    )
    P3 = random.choice(P3_val)
    P4 = ""
    P5 = ""
    P6 = ""
    P7 = ""
    P8 = ""
    P9 = random.choice(P9_val)
    P10 = ""
    P11 = 0
    P12 = fake.random_int(min=0, max=1)
    P13 = 0
    P14 = 0
    P15 = fake.random_int(min=0, max=1)
    P16 = 0
    P17 = fake.random_int(min=0, max=1)
    P18 = 0
    P19 = 0
    P20 = 0

    # Insert data into the table
    cursor.execute(
        """
        INSERT INTO message_information
        (EType, Id, Fb, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            EType,
            Id,
            Fb,
            P1,
            P2,
            P3,
            P4,
            P5,
            P6,
            P7,
            P8,
            P9,
            P10,
            P11,
            P12,
            P13,
            P14,
            P15,
            P16,
            P17,
            P18,
            P19,
            P20,
        ),
    )

# Commit the changes and close the connection
conn.commit()
conn.close()

## Note: Line of code added to find the database link.
## Will make changes to the database using the GUI, in this case DB Browser for SQLite

database_filename = "message.db"

current_directory = os.getcwd()
database_path = os.path.join(current_directory, database_filename)

print("Database path: ", database_path)
