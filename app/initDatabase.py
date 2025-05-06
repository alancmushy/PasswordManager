import sqlite3

def startup():
    connection = sqlite3.connect('passwordDatabase.db')

    with open('app\passProtect.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()
    #print("Database successfully created")
    connection.commit()
    connection.close()

    