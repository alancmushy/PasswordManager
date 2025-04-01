import sqlite3
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import re
import os
from dotenv import load_dotenv
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.keywrap import aes_key_wrap, aes_key_unwrap

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

def userSelection(user):
   print("type 1 if you want to view passwords or 2 if you want to add a password or 3 to log out")
   select = input("Type number here: ")
   if select == "1":
      userPortal(user)
   if select == "2":
      addPassword(user)
   if select == "3":
      startup()

def genSalt():
   salt = os.urandom(16)
   return salt


def kdfMaster(password,user):
   kdf = Scrypt(
    salt=genSalt(),
    length=24,
    n=2**14,
    r=8,
    p=1,
   )
   mKey = kdf.derive(password.encode())
   with open(".env", "a") as f:
      f.write(f"{user}={mKey.hex()}\n")



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
   kdfMaster(password,username)
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
               userSelection(username)
               break
         except VerifyMismatchError:
            print("Password for user is incorrect")
      else:
         print("User does not exist try again")
  
def passwordCheck(pswd):
   while not (any(i.isdigit() for i in pswd) and regex.search(pswd)):
      print("Password not strong enough")
      pswd = input ("Enter password: ")
      passwordCheck(pswd)
   return pswd

def hashPassword(password):
   pswdHashed = hasher.hash(password)
   return pswdHashed

def genEncryptionKey():
   return get_random_bytes(16)


def keyWrapping(user,eKey):
   load_dotenv()
   mKeydata = os.getenv(user)
   mKey = bytes.fromhex(mKeydata)
   key = aes_key_wrap(mKey,eKey)
   return key

def keyUnwrapping(user,wKey):
   load_dotenv()
   mKeydata = os.getenv(user)
   mKey = bytes.fromhex(mKeydata)
   key = aes_key_unwrap(mKey,wKey)
   return key

def encryptPassword(password,key,header):
   header = header.encode()
   password = password.encode()
   cipher = AES.new(key, AES.MODE_GCM)
   cipher.update(header)
   ciphertext, tag = cipher.encrypt_and_digest(password)
   encryption = cipher.nonce + b"EUREKA" + ciphertext + b"EUREKA" + tag
   print(encryption)
   return encryption
   
def decryptPassword(nonce, ciphertext, tag, key,header):
   header = header.encode()
   cipher = AES.new(key, AES.MODE_GCM, nonce)
   cipher.update(header)
   plaintext = cipher.decrypt_and_verify(ciphertext, tag)
   plaintext = plaintext.decode()
   return plaintext

def addPassword(user):
   passwordUser = input ("Enter password username: ")
   passwordPlaintext = input ("Enter password: ")
   website = input ("Enter password website: ")
   key = genEncryptionKey()
   ePassword = encryptPassword(passwordPlaintext,key,website)
   wKey = keyWrapping(user, key)
   connCursor.execute("INSERT INTO usersPasswords (user, passwordUsername, passwordWebsite, passwordData, wrappedKey) VALUES (? ,? , ?, ?, ?)", (user, passwordUser, website, ePassword, wKey))
   print(user + "'s " + website + " password successfully added to database")
   connection.commit()
   userSelection(user)

def userPortal(user):
   connCursor.execute("SELECT passwordData FROM usersPasswords WHERE user = ?", (user,))
   passwords = connCursor.fetchall()
   print(user + "'s Passwords:")
   for password in passwords:
      connCursor.execute("SELECT passwordUsername, passwordWebsite, wrappedKey FROM usersPasswords WHERE passwordData = ?", (password[0],))
      result = connCursor.fetchone()
      print(result)
      username = result[0]
      website = result[1]
      wKey = result[2]
      key = keyUnwrapping(user,wKey)
      password_data = password[0].split(b'EUREKA')
      plainPassword = decryptPassword(password_data[0],password_data[1],password_data[2],key,website)
      print("Website: " + website + ", Username: " + username + ", Password: " + plainPassword)
   userSelection(user)

startup()