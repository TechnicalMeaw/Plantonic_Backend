from fastapi import FastAPI
from .database import engine
from .routers import auth, delivery, homepage
from .blue_dart import api


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(delivery.router)
app.include_router(homepage.router)


# api.track_shipment('80401604146')