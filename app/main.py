from fastapi import *
from app.app_router import router
from app.initDatabase import startup
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
   startup()
   print("Database successfully created")
   yield

app = FastAPI(lifespan=lifespan)


origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://archlock.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)