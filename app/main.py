from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import engine
from .routers import auth, delivery, homepage, profilepage, webpage
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(webpage.router)
app.include_router(auth.router)
app.include_router(delivery.router)
app.include_router(homepage.router)
app.include_router(profilepage.router)


# api.track_shipment('80401604146')