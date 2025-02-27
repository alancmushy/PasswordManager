import sqlite3
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import re

regex = re.compile(r'[^\w\s]|\.')
hasher = PasswordHasher()

connection = sqlite3.connect('passwordDatabase.db', check_same_thread=False)
connCursor = connection.cursor()


def startup():
   print("type 1 if you want to login or 2 if you want to create a user")
   start = input("Type number here: ")
   if start == "1":
      logIn()
   if start == "2":
      createUser()

def createUser():
   print("Create username and password")
   username = input ("Enter username: ")
   connCursor.execute("SELECT 1 FROM users WHERE userName = ?", (username,))
   if connCursor.fetchone():
      print("Username exists already")
      return createUser()
  
   password = input ("Enter password: ")
   passwordCheck(password)
   
   connCursor.execute("INSERT INTO users (userName, pass_hash) VALUES (?, ?)", (username, hashPassword(password)))
   connection.commit()
   print("User created successfully!")
   userPortal(username)
   
def logIn():
   print("Enter Username and Password")

   while True:
      username = input ("Enter username: ")
      password = input ("Enter password: ")
      connCursor.execute("SELECT pass_hash FROM users WHERE userName = ?", (username,))
      currentUser = connCursor.fetchone()
      if currentUser:
         try:
            if(hasher.verify(currentUser[0],password)):
               print("Welcome back")
               userPortal(username)
               break
         except VerifyMismatchError:
            print("Password for user is incorrect")
      else:
         print("User does not exist try again")
  
def passwordCheck(pswd):
   while not (any(i.isdigit() for i in pswd) and regex.search(pswd)):
      print("Password not strong enough")
      print(f"DEBUG: Contains digit? {any(i.isdigit() for i in pswd)}")  
      print(f"DEBUG: Contains special char? {regex.search(pswd) is not None}")
      pswd = input ("Enter password: ")
      passwordCheck(pswd)
   return pswd

def userPortal(user):
   connCursor.execute("SELECT passwordText FROM usersPasswords WHERE user = ?", (user,))
   if connCursor.fetchone():
      print(connCursor.fetchall())
   else:
      print("No password in database! Add password into database")
      addPassword(user)

def hashPassword(password):
   pswdHashed = hasher.hash(password)
   return pswdHashed

def addPassword(user):
   passwordUsername = input ("Enter password username: ")
   password = input ("Enter password: ")
   website = input ("Enter password website: ")
   connCursor.execute("INSERT INTO usersPasswords (user, passwordWebsite, passwordText, passwordUsername) VALUES (? ,? , ?, ?)", (user, website, password, passwordUsername))
   connection.commit()


startup()
