from fastapi import *
from app.app_router import router
from app.initDatabase import startup
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
   startup()
   print("Database successfully created")
   yield

app = FastAPI(lifespan=lifespan)

app.include_router(router)