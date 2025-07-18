from fastapi import *
from app.app_router import router
from app.initDatabase import startup
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):
   startup()
   print("Database successfully created")
   yield

app = FastAPI(lifespan=lifespan)


origins = [
    "http://localhost:5173",
    "https://archlock.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)