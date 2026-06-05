from typing import List
from fastapi import FastAPI
import models
from database import engine
from dependencies import df_dependency, db_dependency
from filldb import init_db
from routers import (guests, revenues, searches, stats)
from response_models import BookingDBModel

app = FastAPI()

app.include_router(stats.router)
app.include_router(guests.router)
app.include_router(revenues.router)
app.include_router(searches.router)

models.Base.metadata.create_all(bind=engine)

init_db()


@app.get("/")
def root():
    return 'Try visiting /docs for all methods and endpoints'


@app.get("/bookings")  # DB
def bookings(db: db_dependency) -> List[BookingDBModel]:
    return db.query(models.Bookings).all()
