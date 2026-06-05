from typing import List, Annotated

from fastapi import APIRouter, status, Depends
from dependencies import df_dependency, db_dependency
from pandas import to_datetime
from response_models import (BookingStatsModel, BookingAnalysisModel, MealPopularityModel,
                             CountriesPopularityModel, AverageADRMonthModel, CommonWeekdayModel,
                             BookingMealHotelModel, AverageLengthOfStayByYearModel, AverageLengthOfStayByHotelModel,
                             MonthBookingsTrendsModel, DistributionTrendsModel, RoomTrendsModel)
from auth import get_current_username


router = APIRouter(prefix='/bookings', tags=['statistics'])


@router.get("/stats",
            summary="Get statistics about bookings",
            response_description='Min, mean and max information about numeric values',
            status_code=status.HTTP_200_OK)
def booking_stats(df: df_dependency) -> BookingStatsModel:
    """
    **return**: json filled with min, mean anx max values for
    - **lead_time** - days, elapsed between booking and arrival date
    - **total_days_stayed** - amount of days spent in hotel
    - **adr** - average daily rate
    - **days_in_waiting_list** - number of days booking was in waiting list before confirmation
    """
    df['total_days_stayed'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    aggregated = df[['lead_time', 'total_days_stayed', 'adr', 'days_in_waiting_list']].agg(['min', 'mean', 'max'])
    return aggregated.to_dict()


@router.get("/analysis",
            summary="Get some trends of dataset",
            response_description='Months, guest demographic, meal, distribution channel, room type trends',
            status_code=status.HTTP_200_OK)
def booking_analysis(df: df_dependency) -> BookingAnalysisModel:
    month_trends = df.groupby('arrival_date_month').size()

    guest_trends = df.groupby('country').size().nlargest(5)

    meal_trends = df.groupby('meal').size()

    distribution_trends = df.groupby('distribution_channel').size()

    room_trends = df.groupby('reserved_room_type').size().nlargest(3)

    return BookingAnalysisModel(
        month_trends=[MonthBookingsTrendsModel(month=k, bookings=v) for k, v in month_trends.to_dict().items()],
        guest_trends=[CountriesPopularityModel(country_name=k, bookings=v) for k, v in guest_trends.to_dict().items()],
        meal_trends=[MealPopularityModel(meal_type=k, appears=v) for k, v in meal_trends.to_dict().items()],
        distribution_channel_trends=[DistributionTrendsModel(distribution_channel=k, bookings=v) for k, v in distribution_trends.to_dict().items()],
        room_trends=[RoomTrendsModel(room_type=k, bookings=v) for k, v in room_trends.to_dict().items()]
    )


@router.get("/popular_meal_package",
            summary="Get most popular meal package",
            response_description='Most popular meal package',
            status_code=status.HTTP_200_OK)
def booking_popular_meal_package(df: df_dependency) -> MealPopularityModel:
    local_df = df.groupby(['meal']).size().nlargest(1).to_dict()

    meal = list(local_df.keys())[0]
    amount = list(local_df.values())[0]

    return MealPopularityModel(meal_type=meal, amount=amount)


@router.get("/avg_length_of_stay",
            summary="Get average length of stay",
            response_description='Average length of stay grouped by arrival date and hotel',
            status_code=status.HTTP_200_OK)
def booking_avg_length_of_stay(df: df_dependency) -> List[AverageLengthOfStayByYearModel]:
    df['total_days_stayed'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    local_df = df.groupby(['arrival_date_year', 'hotel'])['total_days_stayed'].mean().unstack().to_dict(orient='index')

    return [AverageLengthOfStayByYearModel(year=year, avg_hotels=
    [AverageLengthOfStayByHotelModel(hotel_name=k, length_of_stay=v) for k, v in avgs.items()])
            for year, avgs in local_df.items()]


@router.get("/top_countries",
            summary="Get top countries",
            response_description='Top 5 countries by bookings',
            status_code=status.HTTP_200_OK)
def booking_top_countries(df: df_dependency) -> List[CountriesPopularityModel]:
    local_df = df.groupby(['country']).size().nlargest(5)
    return [CountriesPopularityModel(country_name=k, bookings=v) for k, v in local_df.to_dict().items()]


@router.get("/average_daily_rate_resort",
            summary="Get average daily rate in resort hotel",
            response_description='Average daily rate in resort hotel grouped by booking month',
            status_code=status.HTTP_200_OK)
def booking_average_guests_by_year(df: df_dependency, username: Annotated[str, Depends(get_current_username)]) -> List[AverageADRMonthModel]:
    local_df = df[df['hotel'].str.casefold() == 'resort hotel'].groupby(['arrival_date_month'])['adr'].mean()
    return [AverageADRMonthModel(month=k, av_adr=v) for k, v in local_df.to_dict().items()]


@router.get("/most_common_arrival_day_city",
            summary="Get most common arrival weekday in city hotel",
            response_description='Most common arrival weekday in city hotel',
            status_code=status.HTTP_200_OK)
def booking_most_common_arrival_day_city(df: df_dependency, username: Annotated[str, Depends(get_current_username)]) -> CommonWeekdayModel:
    df['date'] = to_datetime(df['arrival_date_year'].astype(str) + ' ' + df['arrival_date_month'].astype(str)
                             + ' ' + df['arrival_date_day_of_month'].astype(str))

    df['arrival_date_day_of_week'] = df['date'].dt.day_name()

    local_df = df['arrival_date_day_of_week'].value_counts()
    day = local_df.idxmax()

    return CommonWeekdayModel(day=day, appears=local_df[day])


@router.get("/count_by_hotel_meal",
            summary="Get count of booked meals",
            response_description='Count of meals grouped by hotel',
            status_code=status.HTTP_200_OK)
def booking_count_by_hotel_meal(df: df_dependency, username: Annotated[str, Depends(get_current_username)]) -> List[BookingMealHotelModel]:
    local_df = df.groupby(['hotel', 'meal']).size().unstack().fillna(0).to_dict(orient='index')

    return [BookingMealHotelModel(hotel_name=hotel,
                                  meals=[MealPopularityModel(meal_type=k, appears=v) for k, v in meal.items()])
            for hotel, meal in local_df.items()]
