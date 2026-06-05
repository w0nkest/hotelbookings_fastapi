from dependencies import db_dependency, df_dependency, get_db, get_df
import pandas as pd
from sqlalchemy import delete
import models
from database import engine


def clear_db(db: db_dependency):
    q = delete(models.Bookings)
    db.execute(q)
    db.commit()


def fill_db(db: db_dependency, df: df_dependency):
    local_df = pd.DataFrame()
    local_df['guest_name'] = df['name']
    local_df['length_of_stay'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    local_df['booking_date'] = pd.to_datetime(
        df['arrival_date_year'].astype(str) + ' ' + df['arrival_date_month'].astype(str)
        + ' ' + df['arrival_date_day_of_month'].astype(str))
    local_df['daily_rate'] = df['adr']
    local_df.to_sql('bookings', con=engine, if_exists='append', index=False)
    db.commit()


def init_db():
    with next(get_db()) as dbiter:
        clear_db(dbiter)
        fill_db(dbiter, get_df())
