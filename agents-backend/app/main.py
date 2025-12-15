from fastapi import FastAPI
from app.api.run import router
from dotenv import load_dotenv
import time
from fastapi import Request
from app.core.logging import logger

load_dotenv()

app = FastAPI()
app.include_router(router, prefix="/agent")

@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start

    logger.info(
        f"[API] {request.method} {request.url.path} "
        f"status={response.status_code} "
        f"time={elapsed:.2f}s"
    )

    response.headers["X-Response-Time"] = str(elapsed)
    return response