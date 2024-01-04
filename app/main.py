from fastapi import FastAPI
from .database import engine
from .routers import auth, delivery, homepage


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(delivery.router)
app.include_router(homepage.router)