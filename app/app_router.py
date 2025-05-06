from fastapi import APIRouter,FastAPI
from contextlib import *
from app.logic import *


router = APIRouter()
logic = App()
app = FastAPI()

@router.get("/")
def root():
   return "Welcome To ArchLock"

@router.post("/login", response_model= User)
def login_user(login_user:User):
   print("Login function")
   return logic.logIn(login_user)

@router.post("/register", response_model= User)
def register_user(created_user:User):
   print("Register function")
   return logic.createUser(created_user)

@router.post("/{loggedInUser}/append")
def add_password(addedPswd:dbData, loggedInUser: str):
   print("Add password function")
   return logic.addPassword(addedPswd,loggedInUser)

@router.get("/{loggedInUser}/view")
def view_passwords(loggedInUser:str):
   print("user portal function")
   return logic.userPortal(loggedInUser)

