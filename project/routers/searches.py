from fastapi import APIRouter, HTTPException, Path, status
from typing import Union, List
from datetime import datetime
import models
from response_models import BookingDBModel, NationalityBookingModel
from dependencies import df_dependency, db_dependency

router = APIRouter(prefix="/bookings", tags=["searching"])


@router.get("/search",
            summary='Searches for bookings',
            response_description='Bookings, that suits given parameters',
            status_code=status.HTTP_200_OK)  # DB
def search_booking(db: db_dependency,
                   guest_name: Union[str, None] = None,
                   booking_date: Union[datetime, None] = None,
                   length_of_stay: Union[int, None] = None) -> List[BookingDBModel]:
    """
    Searches for booking with given parameters, if none is provided returns 404 exception
    - **db**: database connection
    - **guest_name**: name of the guest, optional
    - **booking_date**: Date of the booking, optional, format: YYYY-MM-DD
    - **length_of_stay**: length of stay in days, optional
    - **return**: json, contains suitable data
    """

    if all(_ is None for _ in [guest_name, booking_date, length_of_stay]):
        raise HTTPException(status_code=404, detail="None of parameters were provided")

    objs = db.query(models.Bookings)

    if guest_name is not None:
        objs = objs.filter(models.Bookings.guest_name == guest_name)
    if booking_date is not None:
        objs = objs.filter(models.Bookings.booking_date == booking_date)
    if length_of_stay is not None:
        objs = objs.filter(models.Bookings.length_of_stay == length_of_stay)

    return objs.all()


@router.get("/nationality",
            summary='Searches for bookings with presented nationality',
            response_description='Booking, that suits provided nationality',
            status_code=status.HTTP_200_OK)
def booking_nationality(df: df_dependency, nationality: str) -> List[NationalityBookingModel]:
    local_df = df[df['country'].str.casefold() == nationality.casefold()]

    return [NationalityBookingModel(
        **_
    ) for _ in local_df.to_dict(orient='records')]


@router.get("/{booking_id}",
            summary='Searches for booking with provided id',
            response_description='Booking, that suits provided id',
            status_code=status.HTTP_200_OK)  # DB
def booking_by_id(db: db_dependency, booking_id: int = Path(gt=0)) -> BookingDBModel:
    obj = db.query(models.Bookings).filter(models.Bookings.id == booking_id).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return obj
