import os
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd


def get_new_data(year: int, month: int) -> pd.DataFrame:
    """
    Downloads new data from https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata
    according to given year and month.
    """
    if month < 1 or month > 12 or year < 2009 or year > 2021:
        raise f"No data available for year={year} and month={month}."
    df = pd.read_csv(f"https://s3.amazonaws.com/nyc-tlc/trip+data/"
                     f"yellow_tripdata_{year}-{str(month).zfill(2)}.csv")
    df.to_csv(os.path.join("data", f"yellow_tripdata_{year}-{str(month).zfill(2)}.csv"))
    return df


def data_exists(year: int, month: int) -> bool:
    """
    Check if data for a specific year and month have been downloaded already.
    """
    if f"yellow_tripdata_{year}-{str(month).zfill(2)}.csv" in os.listdir('data'):
        return True
    return False


def get_data(year: int, month: int) -> pd.DataFrame:
    """
    Get data from local storage either or download from url.
    """
    if data_exists(year, month):
        return pd.read_csv(os.path.join("data", f"yellow_tripdata_{year}-{str(month).zfill(2)}.csv"))
    else:
        return get_new_data(year, month)


def average_trip_length(year: int, month: int) -> float:
    """
    Calculates the average trip length of all Yellow Taxis
    for a given year and month.
    """
    data = get_data(year, month)
    #return (pd.to_datetime(data.tpep_dropoff_datetime)
    #        - pd.to_datetime(data.tpep_pickup_datetime)).mean()
    return data.trip_distance.mean()


def rolling_average(year: int,
                    month: int,
                    day: int,
                    time_delta: int) -> datetime:
    """
    A given date and time_delta in days, compute the average trip_distance for all
    yellow cab trips inside this time period.
    """
    # TODO: does not work for time periods in  single month
    start_date = datetime.date(year=year, month=month, day=day)
    end_date = start_date + datetime.timedelta(days=time_delta)
    df_s = get_data(year, month)
    df_s = df_s[pd.to_datetime(df_s.tpep_dropoff_datetime) >= datetime.datetime(start_date.year,
                                                                                start_date.month,
                                                                                start_date.day)]
    df_e = get_data(end_date.year, end_date.month)
    df_e = df_e[pd.to_datetime(df_e.tpep_dropoff_datetime) <= datetime.datetime(end_date.year,
                                                                                end_date.month,
                                                                                end_date.day)]
    df_final = pd.concat([df_s, df_e])
    # in case the time_delta covers 3 months
    # TODO works for 45 days, but not for more than 3 months
    middle_month = start_date + relativedelta(months=1)
    if end_date.month != middle_month.month:
        df_m = get_data(middle_month.year, middle_month.month)
        df_final = pd.concat([df_final, df_m])
    return df_final.trip_distance.mean()


print(f"Average trip length in February 2021 was {average_trip_length(2021, 1)}")
print(f"45 days rolling average on Jan first 2021 was {rolling_average(2021, 1, 1, 45)}")
