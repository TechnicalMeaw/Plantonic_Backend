from fastapi import FastAPI, Request
from . import models
from .database import engine
from .routers import auth, webpage, payment, payments

from fastapi.staticfiles import StaticFiles


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Webpage
app.include_router(webpage.router)

# Auth
app.include_router(auth.router)

# Payment
# app.include_router(payment.router)
app.include_router(payments.router)

