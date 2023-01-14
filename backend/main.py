from dotenv import load_dotenv
load_dotenv('backend/backend.env')

from fastapi import FastAPI
from auth.route import authRouter

app = FastAPI()
app.include_router(authRouter)