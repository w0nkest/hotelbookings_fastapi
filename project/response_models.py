from datetime import datetime
from typing import List

from pydantic import BaseModel


class BookingDBModel(BaseModel):
    id: int = 14
    booking_date: datetime = datetime.now()
    length_of_stay: int = 8
    guest_name: str = "Vasilii Petrovich"
    daily_rate: float = 14.8


class BookingStatsModel(BaseModel):
    class MinMeanMaxStats(BaseModel):
        min: float = 8
        mean: float = 11
        max: float = 14

    lead_time: MinMeanMaxStats
    total_days_stayed: MinMeanMaxStats
    adr: MinMeanMaxStats
    days_in_waiting_list: MinMeanMaxStats


class MealPopularityModel(BaseModel):
    meal_type: str = 'meal_type'
    appears: int = 8


class CountriesPopularityModel(BaseModel):
    country_name: str = 'RUS'
    bookings: int = 14


class AverageADRMonthModel(BaseModel):
    month: str = 'January'
    av_adr: float = 14.8


class CommonWeekdayModel(BaseModel):
    day: str = 'Monday'
    appears: int = 8


class BookingMealHotelModel(BaseModel):
    hotel_name: str = 'Resort Hotel'
    meals: List[MealPopularityModel]


class AverageLengthOfStayByHotelModel(BaseModel):
    hotel_name: str = 'Resort Hotel'
    length_of_stay: float = 14.8


class AverageLengthOfStayByYearModel(BaseModel):
    year: int = 2014
    avg_hotels: List[AverageLengthOfStayByHotelModel]


class MonthBookingsTrendsModel(BaseModel):
    month: str = 'January'
    bookings: int = 14


class DistributionTrendsModel(BaseModel):
    distribution_channel: str = 'channel'
    bookings: int = 8


class RoomTrendsModel(BaseModel):
    room_type: str = 'type1'
    bookings: int = 14


class BookingAnalysisModel(BaseModel):
    month_trends: List[MonthBookingsTrendsModel]
    guest_trends: List[CountriesPopularityModel]
    meal_trends: List[MealPopularityModel]
    distribution_channel_trends: List[DistributionTrendsModel]
    room_trends: List[RoomTrendsModel]


class RepeatedGuestsPercentageModel(BaseModel):
    percentage_of_repeated_guests: float


class GuestsByYearModel(BaseModel):
    year: int = 2014
    amount: int = 148


class RepeatedGuestsByHotelModel(BaseModel):
    class GuestTypeModel(BaseModel):
        unique: int = 14
        repeated: int = 8

    hotel_name: str = 'Resort Hotel'
    guests: GuestTypeModel


class TotalRevenueModel(BaseModel):
    class HotelRevenuesModel(BaseModel):
        hotel_name: str = 'Resort Hotel'
        revenue: float = 148

    month: str = 'January'
    revenues: List[HotelRevenuesModel]


class RevenueResortsByCountriesModel(BaseModel):
    country: str = 'RUS'
    revenue: float = 148


class NationalityBookingModel(BaseModel):
    hotel: str = 'Resort Hotel'
    is_cancelled: bool = False
    lead_time: int = 14
    arrival_date_year: int = 2014
    arrival_date_month: str = 'January'
    arrival_date_day_of_month: int = 8
    stays_in_weekend_nights: int = 14
    stays_in_week_nights: int = 8
    adults: int = 14
    children: int = 8
    babies: int = 14
    meal: str = 'Meal'
    country: str = 'RUS'
    market_segment: str = 'Market Segment'
    distribution_channel: str = 'Distribution'
    is_repeated_guest: bool = False
    previous_cancellations: int = 8
    previous_bookings_not_cancelled: int = 14
    reserved_room_type: str = 'A'
    assigned_room_type: str = 'A'
    booking_changes: int = 8
    deposit_type: str = 'Deposit'
    agent: int = 14
    days_in_waiting_list: int = 8
    customer_type: str = 'Customer'
    adr: float = 14
    required_car_parking_spaces: int = 8
    total_of_special_requests: int = 14
    reservation_status: str = 'Reservation Status'
    reservation_status_data: datetime = datetime.now()
    name: str = 'Vasilii Petrovich'
    email: str = 'petrovich@ya.ru'
    phone_number: str = '+123456789'
