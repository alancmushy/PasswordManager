import sqlite3
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import re
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

regex = re.compile(r'[^\w\s]|\.')
hasher = PasswordHasher()
userMasterKey = b""

connection = sqlite3.connect('passwordDatabase.db', check_same_thread=False)
connCursor = connection.cursor()


def startup():
   print("type 1 if you want to login or 2 if you want to create a user")
   start = input("Type number here: ")
   if start == "1":
      logIn()
   if start == "2":
      createUser()
   
def genSalt():
   salt = os.urandom(16)
   return salt

def kdfMaster(password,salt):
   kdf = Scrypt(
    salt=salt,
    length=32,
    n=2**14,
    r=8,
    p=1,
   )
   masterKey = kdf.derive(password.encode())
   return masterKey
   


def createUser():
   print("Create username and password")
   username = input ("Enter username: ")
   connCursor.execute("SELECT 1 FROM users WHERE userName = ?", (username,))
   if connCursor.fetchone():
      print("Username exists already")
      return createUser()
  
   password = input ("Enter password: ")
   passwordCheck(password)
   
   connCursor.execute("INSERT INTO users (userName, pass_hash, salt) VALUES (?, ?, ?)", (username, hashPassword(password), genSalt()))
   connection.commit()
   
   
   connCursor.execute("SELECT salt FROM users WHERE userName = ?", (username,))
   newUserSalt = connCursor.fetchone()
   kdfMaster(password, newUserSalt[0])
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
               connCursor.execute("SELECT salt FROM users WHERE userName = ?", (username,))
               currUserSalt = connCursor.fetchone()
               userMasterKey = kdfMaster(password, currUserSalt[0])
               print(userMasterKey)
               print(currUserSalt)
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
   passwords = connCursor.fetchall()
   for password in passwords:
      print(password)
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