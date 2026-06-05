from database import session
from typing import Annotated
import pandas as pd
from sqlalchemy.orm import Session
from fastapi import Depends


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def get_df():
    dataframe = (pd.read_csv('hotel_bookings_data.csv')
    .dropna(
        subset=['hotel', 'arrival_date_year', 'arrival_date_month', 'arrival_date_day_of_month',
                'stays_in_weekend_nights', 'stays_in_week_nights', 'country', 'name', 'reservation_status_date'],
    ))

    dataframe.drop(columns=['arrival_date_week_number', 'company', 'credit_card'], inplace=True)

    dataframe.fillna({'is_cancelled': 0,
                      'is_repeated_guest': 0,
                      'lead_time': int(dataframe['lead_time'].mean()),
                      'meal': 'SC',
                      'adults': int(dataframe['adults'].mean()),
                      'children': int(dataframe['children'].mean()),
                      'babies': int(dataframe['babies'].mean()),
                      'market_segment': 'Online TA',
                      'distribution_channel': 'TA/TO',
                      'previous_cancellations': 0,
                      'previous_booking_not_cancelled': 0,
                      'reserved_room_type': 'A',
                      'assigned_room_type': 'A',
                      'booking_changes': 0,
                      'deposit_type': 'No Deposit',
                      'agent': 0,
                      'days_in_waiting_list': 0,
                      'customer_type': 'Transient',
                      'required_car_parking_spaces': 0,
                      'total_of_special_requests': 0,
                      'reservation_status': 'Check-Out',
                      'email': 'example@emal.com',
                      'phone-number': '000-000-0000',
                      'adr': dataframe['adr'].mean()},
                     inplace=True)
    dataframe['meal'] = dataframe['meal'].replace(['Undefined', 'undefined'], 'SC')
    dataframe.rename(columns={'phone-number': 'phone_number'}, inplace=True)
    return dataframe


df_dependency = Annotated[pd.DataFrame, Depends(get_df)]
