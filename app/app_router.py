from fastapi import APIRouter,Request,Response,HTTPException,Depends 
from uuid import uuid4
from contextlib import *
from app.logic import *
from pydantic import BaseModel
from fastapi.responses import RedirectResponse


router = APIRouter()
logic = App()

class passwordRequest(BaseModel):
   oldPswd: dbData
   newPswd: dbData


sessionval={}
def checkSession(req:Request,username:str):
   id = req.cookies.get("session_id")
   if id not in sessionval or sessionval[id]["username"]!= username:
      print(sessionval)
      raise HTTPException(status_code=401, detail="ACCESS UNAUTHORIZED")
   return("ACCESS AUTHORIZED")

@router.get("/")
def root():
   return "Welcome To ArchLock"


@router.post("/register", response_model= User)
async def register_user(res: Response,created_user:User):
   print("Register function")
   user = logic.createUser(created_user)
   if not(user):
      raise HTTPException(status_code=400, detail="REGISTRATION FAILURE")
   session = str(uuid4())
   sessionval[session] = {"username":user.username}
   res.set_cookie(key="session_id", value=session, httponly=True, secure=True, samesite="None")
   return user


@router.post("/login", response_model= User)
async def login_user(res: Response,login_user:User):
   print("Login function")
   print("user", login_user)
   user = logic.logIn(login_user)
   if not(user):
      raise HTTPException(status_code=400, detail="LOGIN FAILURE")
   session = str(uuid4())
   sessionval[session] = {"username":login_user.username}
   res.set_cookie(key="session_id", value=session, httponly=True, secure=True, samesite="None")
   return user

@router.post("/{loggedInUser}/append")
async def add_password(req:Request, addedPswd:dbData, loggedInUser: str):
   checkSession(req,loggedInUser)
   print("Add password function")
   return logic.addPassword(addedPswd,loggedInUser)

@router.delete("/{loggedInUser}/delete")
async def delete_passwords(req:Request, deletePswd:dbData, loggedInUser:str):
   checkSession(req,loggedInUser)
   print("delete function")
   print("Selected pswd: " , deletePswd)
   return logic.deletePassword(deletePswd,loggedInUser)

@router.get("/{loggedInUser}/view")
async def view_passwords(req:Request,loggedInUser:str):
   checkSession(req,loggedInUser)
   print("user portal function")
   return logic.userPortal(loggedInUser)

@router.post("/{loggedInUser}/update")
async def update_password(req:Request,passwordBundle:passwordRequest,loggedInUser:str,):
   checkSession(req,loggedInUser)
   print("Update function")
   return logic.updatePassword(passwordBundle.oldPswd,passwordBundle.newPswd,loggedInUser)


@router.post("/logout")
def logout_user(req:Request,res:Response):
   id = req.cookies.get("session_id")
   if id in sessionval:
      del sessionval[id]
      res.delete_cookie("session_id")
      return ("LOGOUT SUCCESSFUL")
