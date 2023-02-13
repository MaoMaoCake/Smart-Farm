from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from threading import Thread
from worker.route import run_scheduler


from worker.route import workerRouter
from response.error_codes import ErrorException

load_dotenv('worker.env')

app = FastAPI()
app.include_router(workerRouter)


@app.on_event("startup")
def start_scheduler():
    t = Thread(target=run_scheduler)
    t.start()


@app.exception_handler(ErrorException)
async def custom_exception_handler(request: Request, exc: ErrorException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"Exception Occurred! Reason -> {exc.message}",
                 "successful": exc.successful,
                 "error_code": exc.error_code,
                 "message": exc.message,
                 "status_code": exc.status_code,
                },
    )