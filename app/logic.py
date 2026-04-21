import psycopg2
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import re
import os
import json
from dotenv import load_dotenv
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.keywrap import aes_key_wrap, aes_key_unwrap
from fastapi import *
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta


loggedInUser = ""

load_dotenv()
print(os.getenv("DATABASE_URL"))
connection = psycopg2.connect(os.getenv("DATABASE_URL"))
connCursor = connection.cursor()
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY = 30
REFRESH_TOKEN_EXPIRY = 60 * 24 * 7


class User(BaseModel):
   username:str
   password:str

class dbData(BaseModel):
   user_name:str
   plain_password:str
   website:str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str

def createAccessToken(username: str, mKey: bytes):
    payload = {
        "sub": username,
        "mkey": mKey.hex(),
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRY)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)

def createRefreshToken(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRY)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)

def decodeAccessToken(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        mKey = bytes.fromhex(payload.get("mkey"))
        return username, mKey
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def decodeRefreshToken(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    
class App():

    hasher = PasswordHasher()

    @staticmethod
    def genSalt():
        return os.urandom(16)

    def kdfMaster(self, password: str, username: str):
        """Derive master key from password + stored salt. Never stored anywhere."""
        connCursor.execute("SELECT kdf_salt FROM users WHERE userName = %s", (username,))
        result = connCursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="User not found")

        salt = bytes(result[0])
        kdf = Scrypt(salt=salt, length=24, n=2**14, r=8, p=1)
        return kdf.derive(password.encode())

    def createUser(self, createdUser: User):
        connCursor.execute("SELECT 1 FROM users WHERE userName = %s", (createdUser.username,))
        if connCursor.fetchone():
            raise HTTPException(status_code=401, detail="User already exists")

        self.passwordCheck(createdUser.password)

        salt = self.genSalt()

        connCursor.execute("INSERT INTO users (userName, pass_hash, kdf_salt) VALUES (%s, %s, %s)",(createdUser.username, self.hashPassword(createdUser.password), salt))
        connection.commit()

        return createdUser

    def logIn(self, existingUser: User):
        connCursor.execute("SELECT pass_hash FROM users WHERE userName = %s", (existingUser.username,))
        currentUser = connCursor.fetchone()

        if not currentUser:
            raise HTTPException(status_code=404, detail="User not found")

        try:
            self.hasher.verify(currentUser[0], existingUser.password)
        except VerifyMismatchError:
            raise HTTPException(status_code=401, detail="Incorrect password")

        mKey = self.kdfMaster(existingUser.password, existingUser.username)

        access_token = createAccessToken(existingUser.username, mKey)
        refresh_token = createRefreshToken(existingUser.username)

        connCursor.execute(
            "UPDATE users SET refresh_token = %s WHERE userName = %s",
            (refresh_token, existingUser.username)
        )
        connection.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def refreshSession(self, refresh_token: str, password: str):
        username = decodeRefreshToken(refresh_token)

        connCursor.execute(
            "SELECT refresh_token FROM users WHERE userName = %s", (username,)
        )
        result = connCursor.fetchone()
        if not result or result[0] != refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token mismatch")

        mKey = self.kdfMaster(password, username)
        new_access_token = createAccessToken(username, mKey)

        return {"access_token": new_access_token}

    def passwordCheck(self, pswd: str):
        regex = re.compile(r'[^\w\s]|\.')
        if pswd is None:
            raise HTTPException(status_code=400, detail="Invalid password: No password entered")
        if not (any(i.isdigit() for i in pswd) and regex.search(pswd) and len(pswd) >= 7 and ' ' not in pswd):
            raise HTTPException(status_code=401, detail="Invalid password: Weak password")
        return pswd

    def hashPassword(self, password: str):
        return self.hasher.hash(password)

    @staticmethod
    def genEncryptionKey():
        return get_random_bytes(16)

    @staticmethod
    def encryptPassword(password: str, key: bytes, header: str):
        header = header.encode()
        password = password.encode()
        cipher = AES.new(key, AES.MODE_GCM)
        cipher.update(header)
        ciphertext, tag = cipher.encrypt_and_digest(password)
        return cipher.nonce + b"EUREKA" + ciphertext + b"EUREKA" + tag

    @staticmethod
    def decryptPassword(nonce: bytes, ciphertext: bytes, tag: bytes, key: bytes, header: str):
        header = header.encode()
        cipher = AES.new(key, AES.MODE_GCM, nonce)
        cipher.update(header)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode()

    def addPassword(self, pswd: dbData, token: str):
        username, mKey = decodeAccessToken(token)
        key = self.genEncryptionKey()
        ePassword = self.encryptPassword(pswd.plain_password, key, pswd.website)
        wKey = aes_key_wrap(mKey, key)
        connCursor.execute("INSERT INTO usersPasswords (masterUsername, passwordUsername, passwordWebsite, passwordData, wrappedKey) VALUES (%s, %s, %s, %s, %s)",(username, pswd.user_name, pswd.website, ePassword, wKey)
        )
        connection.commit()
        return f"{username}'s {pswd.website} password successfully added"

    def deletePassword(self, pswd: dbData, token: str):
        username, _ = decodeAccessToken(token)
        connCursor.execute("DELETE FROM usersPasswords WHERE masterUsername = %s AND passwordUsername = %s AND passwordWebsite = %s",(username, pswd.user_name, pswd.website)
        )
        connection.commit()
        return "password deleted"

    def updatePassword(self, oldPswd: dbData, newPswd: dbData, token: str):
        username, mKey = decodeAccessToken(token)
        connCursor.execute("SELECT wrappedKey FROM usersPasswords WHERE masterUsername = %s AND passwordUsername = %s AND passwordWebsite = %s",(username, oldPswd.user_name, oldPswd.website))
        data = connCursor.fetchone()
        if not data:
            raise HTTPException(status_code=404, detail="Password not found")

        userKey = data[0]
        unwrappedKey = aes_key_unwrap(mKey, bytes(userKey))
        newPswdData = self.encryptPassword(newPswd.plain_password, unwrappedKey, newPswd.website)
        connCursor.execute("UPDATE usersPasswords SET passwordUsername = %s, passwordWebsite = %s, passwordData = %s WHERE masterUsername = %s AND wrappedKey = %s",(newPswd.user_name, newPswd.website, newPswdData, username, userKey))
        connection.commit()
        return "password updated"

    def userPortal(self, token: str):
        username, mKey = decodeAccessToken(token)
        connCursor.execute("SELECT passwordUsername, passwordWebsite, passwordData, wrappedKey FROM usersPasswords WHERE masterUsername = %s",(username,))
        rows = connCursor.fetchall()
        password_list = []
        for row in rows:
            p_username, website, password_data, wKey = row
            key = aes_key_unwrap(mKey, bytes(wKey))
            parts = bytes(password_data).split(b'EUREKA')
            plainPassword = self.decryptPassword(parts[0], parts[1], parts[2], key, website)
            password_list.append(dbData(
                user_name=p_username,
                plain_password=plainPassword,
                website=website
            ))
        return password_list