import pandas as pd

path = 'project/hotel_bookings_data.csv'

df = pd.read_csv(path)

# --------------------------------

# TASK 1
# What are the top 5 most common last name in the dataset?
# Bonus: Can you figure this out in one line of pandas code?
print(pd.Series(df['name'].str.split().apply(lambda x: x[-1]), name='lastname')
      .value_counts().nlargest(5))
# values in "Final_project_task" and here are different, but I checked this data in Excel and mine are right

# --------------------------------

# TASK 2
# What are the names of the people who had booked the most number
# children and babies for their stay?
df['total_kids'] = df['children'] + df['babies']
print(df.nlargest(3, 'total_kids')
      [['name', 'adults', 'total_kids', 'babies', 'children']])

# --------------------------------

# TASK 3
# How many arrivals took place between the 1st and the 15th of the month
# (inclusive of 1 and 15) ? Can you do this in one line of pandas code?
print(len(df[(1 <= df['arrival_date_day_of_month']) & (df['arrival_date_day_of_month'] <= 15)]))

# --------------------------------

# TASK 4
# Create a table for counts for each day of the week that people arrived.
weekdays = (pd.to_datetime(df['arrival_date_year'].astype(str)
                             + ' ' + df['arrival_date_month'].astype(str)
                             + ' ' + df['arrival_date_day_of_month'].astype(str))).dt.day_name().value_counts()
print(weekdays)

