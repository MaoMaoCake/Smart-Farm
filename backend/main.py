from fastapi import FastAPI
from auth.route import authRouter

from dotenv import load_dotenv
load_dotenv('backend.env')

app = FastAPI()
app.include_router(authRouter)
