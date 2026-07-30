import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import (
    companies,
    documents,
    health,
    peers,
    portfolio,
    screener,
    sectors,
    valuation,
)

app = FastAPI(
    title="N100 Financial Intelligence API",
    version="1.0.0",
)


start_time = time.time()


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_logger(request: Request, call_next):
    """
    Log request method, path and response time.
    """

    start = time.time()

    response = await call_next(request)

    duration = time.time() - start

    logger.info(f"{request.method} " f"{request.url.path} " f"{duration:.4f}s")

    return response


PREFIX = "/api/v1"


app.include_router(health.router, prefix=PREFIX)

app.include_router(companies.router, prefix=PREFIX)

app.include_router(screener.router, prefix=PREFIX)

app.include_router(sectors.router, prefix=PREFIX)

app.include_router(peers.router, prefix=PREFIX)

app.include_router(valuation.router, prefix=PREFIX)

app.include_router(portfolio.router, prefix=PREFIX)

app.include_router(documents.router, prefix=PREFIX)


@app.get("/")
def root():
    """Function: root"""
    return {"message": "N100 Financial Intelligence API", "version": "1.0.0"}
