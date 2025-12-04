import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from app.routes import files
import os
from dotenv import load_dotenv

load_dotenv()
SENTRY_DSN = os.getenv("SENTRY_DSN")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=1.0
)

app = FastAPI()

app.add_middleware(SentryAsgiMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files.router)
