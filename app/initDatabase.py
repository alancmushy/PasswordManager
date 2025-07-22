import psycopg2
import os
def startup():
    
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = connection.cursor()
    with open('app/passProtect.sql') as f:
        tablelines = f.read().split(";")
        for line in tablelines:
            line = line.strip()
            if line:
                cur.execute(line)

    #print("Database successfully created")
    connection.commit()
    connection.close()

    