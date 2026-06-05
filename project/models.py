from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Float


class Bookings(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_date = Column(DateTime)
    length_of_stay = Column(Integer)
    guest_name = Column(String)
    daily_rate = Column(Float)
