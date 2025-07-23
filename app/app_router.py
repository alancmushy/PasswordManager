from fastapi import APIRouter,FastAPI
from contextlib import *
from app.logic import *
from pydantic import BaseModel
from starlette.requests import Request

router = APIRouter()
logic = App()

class passwordRequest(BaseModel):
   oldPswd: dbData
   newPswd: dbData

@router.get("/")
def root():
   return "Welcome To ArchLock"

@router.post("/login", response_model= User)
def login_user(login_user:User):
   print("Login function")
   print("user", login_user)
   return logic.logIn(login_user)

@router.post("/register", response_model= User)
def register_user(created_user:User):
   print("Register function")
   return logic.createUser(created_user)

@router.post("/{loggedInUser}/append")
def add_password(addedPswd:dbData, loggedInUser: str):
   print("Add password function")
   return logic.addPassword(addedPswd,loggedInUser)

@router.delete("/{loggedInUser}/delete")
def delete_passwords(deletePswd:dbData, loggedInUser:str):
   print("delete function")
   print("Selected pswd: " , deletePswd)
   return logic.deletePassword(deletePswd,loggedInUser)

@router.get("/{loggedInUser}/view")
def view_passwords(loggedInUser:str):
   print("user portal function")
   return logic.userPortal(loggedInUser)


@router.post("/{loggedInUser}/update")
def update_password(passwordBundle:passwordRequest,loggedInUser:str,):
   print("Update function")
   return logic.updatePassword(passwordBundle.oldPswd,passwordBundle.newPswd,loggedInUser)

