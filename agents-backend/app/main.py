from fastapi import FastAPI
from app.api.run import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.include_router(router, prefix="/agent")
