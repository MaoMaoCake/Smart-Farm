from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from auth.route import authRouter
from farm.route import farmRouter
from starlette.middleware.cors import CORSMiddleware

from response.error_codes import ErrorException

from dotenv import load_dotenv
load_dotenv('backend.env')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*', 'localhost:5173', '127.0.0.1:5173'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authRouter)
app.include_router(farmRouter)

@app.exception_handler(ErrorException)
async def custom_exception_handler(request: Request, exc: ErrorException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"Exception Occurred! Reason -> {exc.message}",
                 "successful": exc.successful,
                 "error_code" : exc.error_code,
                 "message" : exc.message,
                 "status_code" : exc.status_code,
                },
    )
