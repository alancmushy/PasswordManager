import sqlite3


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

   connCursor.execute("INSERT INTO users (userName, pass_word) VALUES (?, ?)", (username, password))
   connection.commit()
   print("User created successfully!")
   userPortal(username)
   
def logIn():
   print("Enter Username and Password")

   while True:
      username = input ("Enter username: ")
      password = input ("Enter password: ")
      connCursor.execute("SELECT 1 FROM users WHERE userName = ? AND pass_word = ?", (username, password))
      if(connCursor.fetchone()):
         print("Welcome back")
         userPortal(username)
         break
      else:
         print("User does not exist try again")
  
def passwordCheck(pswd):
   while not any(i.isdigit() for i in pswd):
      print("Password not strong enough")
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

def addPassword(user):
   passwordUsername = input ("Enter password username: ")
   password = input ("Enter password: ")
   website = input ("Enter password website: ")
   connCursor.execute("INSERT INTO usersPasswords (user, passwordWebsite, passwordText, passwordUsername) VALUES (? ,? , ?, ?)", (user, website, password, passwordUsername))
   connection.commit()


startup()
