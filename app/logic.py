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
from fastapi import *
from pydantic import BaseModel



connection = sqlite3.connect('passwordDatabase.db', check_same_thread=False)
connCursor = connection.cursor()

class User(BaseModel):
   username:str
   password:str

class dbData(BaseModel):
   user_name:str
   plain_password:str
   website:str
   

class App():

   hasher = PasswordHasher()

   @staticmethod
   def genSalt():
      salt = os.urandom(16)
      return salt


   def kdfMaster(self,password,username):
      kdf = Scrypt(
      salt=self.genSalt(),
      length=24,
      n=2**14,
      r=8,
      p=1,
      )
      mKey = kdf.derive(password.encode())
      with open(".env", "a") as f:
         f.write(f"{username}={mKey.hex()}\n")


   #REFACTORED
   def createUser(self, createdUser:User):
      connCursor.execute("SELECT 1 FROM users WHERE userName = ?", (createdUser.username,))
      if connCursor.fetchone():
         raise HTTPException(status_code=401, detail="User already exists")
      
      self.passwordCheck(createdUser.password)
      
      connCursor.execute("INSERT INTO users (userName, pass_hash) VALUES (?, ?)", (createdUser.username, self.hashPassword(createdUser.password)))
      connection.commit()
      
      self.kdfMaster(createdUser.password,createdUser.username)
 
      self.userPortal(createdUser.username)
      

      return createdUser
   

   #REFACTORED
   def logIn(self, existingUser:User):
      connCursor.execute("SELECT pass_hash FROM users WHERE userName = ?", (existingUser.username,))
      currentUser = connCursor.fetchone()

      if not currentUser:
        raise HTTPException(status_code=404, detail="User not found")

      try:
         if(self.hasher.verify(currentUser[0],existingUser.password)):
            return existingUser
      except VerifyMismatchError:
         raise HTTPException(status_code=401, detail="Incorrect password")
   
               
      
      
   #REFACTORED
   def passwordCheck(self,pswd:str):
      regex = re.compile(r'[^\w\s]|\.')

      if pswd is None:
        raise HTTPException(status_code=400, detail="Invalid password: No password entered")

      if not (any(i.isdigit() for i in pswd) and regex.search(pswd) and len(pswd)>=7 and ' ' not in pswd):
         raise HTTPException(status_code=401, detail="Invalid password: Weak password")
      return pswd


   def hashPassword(self,password:str):
      pswdHashed = self.hasher.hash(password)
      return pswdHashed
   

   @staticmethod
   def getMKey(username:str):
      load_dotenv(os.path.abspath('.env'))
      mKeydata = os.getenv(username)
      mKey = bytes.fromhex(mKeydata)
      return mKey
   
   
   @staticmethod
   def genEncryptionKey():
      return get_random_bytes(16)


   def keyWrapping(self,username:str,eKey:bytes):
      master = self.getMKey(username)
      key = aes_key_wrap(master,eKey)
      return key

 
   def keyUnwrapping(self,username:str,wKey:bytes):
      master = self.getMKey(username)
      key = aes_key_unwrap(master,wKey)
      return key

   
   @staticmethod
   def encryptPassword(password:str,key:bytes,header:str):
      header = header.encode()
      password = password.encode()
      cipher = AES.new(key, AES.MODE_GCM)
      cipher.update(header)
      ciphertext, tag = cipher.encrypt_and_digest(password)
      encryption = cipher.nonce + b"EUREKA" + ciphertext + b"EUREKA" + tag
      print(encryption)
      return encryption

   @staticmethod 
   def decryptPassword(nonce:bytes, ciphertext:bytes, tag:bytes, key:bytes,header:str):
      header = header.encode()
      cipher = AES.new(key, AES.MODE_GCM, nonce)
      cipher.update(header)
      plaintext = cipher.decrypt_and_verify(ciphertext, tag)
      plaintext = plaintext.decode()
      return plaintext

   def updatePassword(self,oldPswd:dbData,newPswd:dbData,username:str):
      connCursor.execute("SELECT wrappedKey FROM usersPasswords WHERE user = ? AND passwordUsername = ? AND passwordWebsite = ?",(username,oldPswd.user_name, oldPswd.website))
      data = connCursor.fetchone()
      userKey = data[0]
      print("User Key " + userKey.hex())
      unwrappedKey = self.keyUnwrapping(username,userKey)
      newPswdData = self.encryptPassword(newPswd.plain_password,unwrappedKey,newPswd.website)
      connCursor.execute("UPDATE usersPasswords SET passwordUsername = ?, passwordWebsite =?, passwordData =? WHERE user = ? AND wrappedKey =?", (newPswd.user_name,newPswd.website,newPswdData,username,userKey))
      connection.commit()
      connCursor.execute("SELECT passwordUsername, passwordWebsite, passwordData FROM usersPasswords WHERE user = ? AND wrappedKey =?", (username,userKey))
      result = connCursor.fetchone()
      print("result " , str(result))
      return "updated password: ", str(result)
   
   #REFACTORED
   def addPassword(self,pswd:dbData, username:str):
      key = self.genEncryptionKey()
      ePassword = self.encryptPassword(pswd.plain_password,key,pswd.website)
      wKey = self.keyWrapping(username, key)
      connCursor.execute("INSERT INTO usersPasswords (user, passwordUsername, passwordWebsite, passwordData, wrappedKey) VALUES (? ,? , ?, ?, ?)", (username, pswd.user_name, pswd.website, ePassword, wKey))
      connection.commit()
      return username + "'s " + pswd.website + " password successfully added to database"
   
   def deletePassword(self,pswd:dbData,username:str):
      connCursor.execute("DELETE FROM usersPasswords WHERE user = ? AND passwordUsername = ? AND passwordWebsite = ?",(username,pswd.user_name,pswd.website))
      connection.commit()
      return "password deleted"

   #REFACTORED
   def userPortal(self,loggedIn:str):
      connCursor.execute("SELECT passwordData FROM usersPasswords WHERE user = ?", (loggedIn,))
      passwords = connCursor.fetchall()
      password_list = []
      for password in passwords:
         connCursor.execute("SELECT passwordUsername, passwordWebsite, wrappedKey FROM usersPasswords WHERE passwordData = ?", (password[0],))
         result = connCursor.fetchone()
         username = result[0]
         website = result[1]
         wKey = result[2]
         key = self.keyUnwrapping(loggedIn,wKey)
         password_data = password[0].split(b'EUREKA')
         plainPassword = self.decryptPassword(password_data[0],password_data[1],password_data[2],key,website)
         pswdDetails = dbData(
            user_name=username,
            plain_password=plainPassword,
            website=website
            )
         password_list.append(pswdDetails)
      return password_list

