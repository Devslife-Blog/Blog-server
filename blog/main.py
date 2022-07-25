from fastapi import FastAPI
from sqlalchemy.orm import Session

from . import database

app = FastAPI(name="Devslife Blog", version="1.0")


@app.on_event('startup')
def on_startup():
    database.Base.metadata.create_all(bind=database.engine)
    db: Session = database.SessionLocal
