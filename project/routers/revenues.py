from fastapi import APIRouter, status, Depends

from auth import get_current_username
from dependencies import df_dependency, db_dependency
from response_models import TotalRevenueModel, RevenueResortsByCountriesModel
from typing import List, Annotated

router = APIRouter(prefix="/bookings", tags=["revenues"])


@router.get("/total_revenue",
            summary="Calculates revenue",
            response_description="Total revenue grouped by booking month and hotel type",
            status_code=status.HTTP_200_OK, )
def booking_revenue(df: df_dependency) -> List[TotalRevenueModel]:
    df['revenue_per_book'] = df['adr'] * (df['stays_in_weekend_nights'] + df['stays_in_week_nights'])
    local_df = (df.groupby(['arrival_date_month', 'hotel'])['revenue_per_book'].sum().unstack()
                .fillna(0).to_dict(orient='index'))

    return [TotalRevenueModel(month=k, revenues=
    [TotalRevenueModel.HotelRevenuesModel(hotel_name=hotel, revenue=rev) for hotel, rev in v.items()])
            for k, v in local_df.items()]


@router.get("/total_revenue_resort_by_country",
            summary="Calculates Resort hotel revenue",
            response_description="Resort hotel revenue grouped by country of visitors",
            status_code=status.HTTP_200_OK)
def booking_total_revenue_resort_by_country(df: df_dependency, username: Annotated[str, Depends(get_current_username)]) -> List[RevenueResortsByCountriesModel]:
    df['revenue_per_book'] = df['adr'] * (df['stays_in_weekend_nights'] + df['stays_in_week_nights'])
    local_df = df[df['hotel'].str.casefold() == 'resort hotel']
    local_df = local_df.groupby(['country'])['revenue_per_book'].sum().to_dict()

    return [RevenueResortsByCountriesModel(country=k, revenue=v) for k, v in local_df.items()]
