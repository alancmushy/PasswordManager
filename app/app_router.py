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
   print("ACCESS AUTHORIZED")
   return id

def getToken(req: Request, username: str):
    # try cookie session first
    id = req.cookies.get("session_id")
    if id and id in sessionval and sessionval[id]["username"] == username:
        token = sessionval[id].get("token")
        if token:
            return token
    
    # fall back to Authorization header
    auth = req.headers.get("authorization")
    if auth and auth.startswith("Bearer "):
        return auth.split(" ")[1]
    
    raise HTTPException(status_code=401, detail="ACCESS UNAUTHORIZED")

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
   res.set_cookie(key="session_id", value=session, httponly=True, secure=True, samesite="lax")
   return user


@router.post("/login", response_model= TokenResponse)
async def login_user(res: Response,login_user:User):
   print("Login function")
   print("user", login_user)
   tokens = logic.logIn(login_user)
   if not tokens:
        raise HTTPException(status_code=400, detail="LOGIN FAILURE")
   session = str(uuid4())
   sessionval[session] = {"username":login_user.username}
   res.set_cookie(key="session_id", value=session, httponly=True, secure=True, samesite="None")
   return tokens

@router.post("/{loggedInUser}/append")
async def add_password(req:Request, addedPswd:dbData, loggedInUser: str):
   token = getToken(req, loggedInUser)
   print("Add password function")
   return logic.addPassword(addedPswd,token)

@router.delete("/{loggedInUser}/delete")
async def delete_passwords(req:Request, deletePswd:dbData, loggedInUser:str):
   token = getToken(req, loggedInUser)
   print("delete function")
   print("Selected pswd: " , deletePswd)
   return logic.deletePassword(deletePswd,token)

@router.get("/{loggedInUser}/view")
async def view_passwords(req:Request,loggedInUser:str):
   token = getToken(req, loggedInUser)
   print("user portal function")
   return logic.userPortal(token)

@router.post("/{loggedInUser}/update")
async def update_password(req:Request,passwordBundle:passwordRequest,loggedInUser:str,):
   token = getToken(req, loggedInUser)
   print("Update function")
   return logic.updatePassword(passwordBundle.oldPswd,passwordBundle.newPswd,loggedInUser,token)


@router.post("/logout")
def logout_user(req:Request,res:Response):
   id = req.cookies.get("session_id")
   if id in sessionval:
      del sessionval[id]
      res.delete_cookie("session_id")
      return ("LOGOUT SUCCESSFUL")
