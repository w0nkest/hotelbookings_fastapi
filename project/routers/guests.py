from fastapi import APIRouter, status, Depends

from auth import get_current_username
from dependencies import df_dependency, db_dependency
from response_models import RepeatedGuestsPercentageModel, GuestsByYearModel, RepeatedGuestsByHotelModel
from typing import List, Annotated

router = APIRouter(prefix="/bookings", tags=["guests_information"])


@router.get("/repeated_guests_percentage",
            summary="Get percentage of guests repeated",
            response_description='Percentage of guests repeated',
            status_code=status.HTTP_200_OK)
def booking_repeated_guests_percentage(df: df_dependency) -> RepeatedGuestsPercentageModel:
    amount_of_repeated = df['is_repeated_guest'].sum()
    amount_of_all = len(df['is_repeated_guest'])
    return RepeatedGuestsPercentageModel(percentage_of_repeated_guests=amount_of_repeated / amount_of_all)


@router.get("/total_guests_by_year",
            summary="Get amount guests by year",
            response_description='Amount of guests grouped by year',
            status_code=status.HTTP_200_OK)
def booking_total_guests_by_year(df: df_dependency) -> List[GuestsByYearModel]:
    df['total_guests'] = (df['adults'] + df['children'] + df['babies']).astype(int)
    local_df = df.groupby(['arrival_date_year'])['total_guests'].sum().to_dict()
    return [GuestsByYearModel(year=k, amount=v) for k, v in local_df.items()]


@router.get('/count_by_hotel_repeated_guest',
            summary="Get amount of unique and repeated guests",
            response_description='Count of unique and repeated guests grouped by hotel',
            status_code=status.HTTP_200_OK)
def booking_count_by_hotel_repeated_guest(df: df_dependency, username: Annotated[str, Depends(get_current_username)]) -> List[RepeatedGuestsByHotelModel]:
    local_df = (df.groupby(['hotel', 'is_repeated_guest']).size()
                .unstack().rename(columns={0: 'unique', 1: 'repeated'}).to_dict(orient='index'))

    print([(k, v) for k, v in local_df.items()])

    return [RepeatedGuestsByHotelModel(hotel_name=hotel,
                                       guests=RepeatedGuestsByHotelModel.
                                       GuestTypeModel(unique=amounts['unique'], repeated=amounts['repeated']))
            for hotel, amounts in local_df.items()]
