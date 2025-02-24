import uvicorn
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api_resto.controllers import index as indexRoute
from api_resto.models import model_loader
from api_resto.dependencies.config import conf
from api_resto.dependencies.database import engine, get_db


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)


if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)
