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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Incoming request: {request.method} {request.url}")
    print(f"Origin: {request.headers.get('origin')}")
    response = await call_next(request)
    return response

app.include_router(router)