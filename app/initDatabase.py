import sqlite3
import os
def startup():
    os.makedirs("data", exist_ok=True)
    connection = sqlite3.connect('data/passwordDatabase.db')

    with open('app/passProtect.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()
    #print("Database successfully created")
    connection.commit()
    connection.close()

    