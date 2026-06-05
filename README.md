# Hotel bookings analysis API

This project represents backend part of any further applications for making analysis of hotel bookings, kept in *hotel_bookings_data.csv* file.
API provides endpoints for retrieving booking data and generating analytical insights from the hotel booking dataset.
- ```/bookings```: retrieve all the bookings from dataset
- ```/bookings/{booking_id}```: retrieve specific booking by provided id
- ```/bookings/search```: search for bookings that suits query parameters
- ```/bookings/stats```: retrieve general statistics about the dataset
- ```/bookings/analysis```: perform advanced data analysis, including trends
- ```/bookings/nationality```: retrieve bookings with nationality, provided as query parameter
- ```/bookings/popular_meal_packages```: retrieve most popular meal package
- ```/bookings/avg_length_of_stay```: retrieve average length of stay grouped by booking year and hotel type
- ```/bookings/total_revenue```: retrieve revenue of hotels grouped by type
- ```/bookings/top_countries```: retrieve top 5 countries by bookings
- ```/bookings/repeated_guest_percentage```: retrieve percentage of repeated guests
- ```/bookings/total_guests_by_year```: retrieve total guest count grouped by booking year
- ```/bookings/avg_daily_rate_resort```: retrieve average ADR by Resort hotel bookings
- ```/bookings/most_common_arrival_date_city```: retrieve most common arrival date of week in City hotel
- ```/bookings/count_by_hotel_meal```: retrieve booking counts grouped by hotel and meal types
- ```/bookings/total_revenue_resort_by_county```: retrieve booking counts grouped by hotel type and repeated guest status

For more detailed information you can visit ```/docs``` endpoint

---

# FastAPI Project Setup

To run the FastAPI server, follow the steps below.

---

## 1. Clone repository


```bash
git clone https://github.com/w0nkest/hotelbookings_fastapi
cd hotelbookings_fastapi
```

---

## 2. Create and activate a virtual environment

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

---

## 3. Go to project folder

```bash
cd project
```

---

## 4. Install required dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Start the FastAPI application

```bash
uvicorn main:app --reload
```

---

# Application URLs

After startup, the server will be available at:

- http://127.0.0.1:8000
- http://localhost:8000

---

# API Documentation

To view all available endpoints and methods, open:

- http://127.0.0.1:8000/docs

To access unavailable methods, that are locked behind username and password, enter
```bash
username: admin
password: 123admin
```

# Tasks are presented in root folder (out of "project" folder), you'll probably see it
```bash
tasks.py
```
