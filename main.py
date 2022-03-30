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
    df.to_csv("data")
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
    start_date = datetime.date(year=year, month=month, day=day)
    end_date = start_date + datetime.timedelta(days=time_delta)
    df_1 = get_data(year, month)
    df_1 = df_1[pd.to_datetime(df_1.tpep_dropoff_datetime) >= start_date]
    df_2 = get_data(end_date.year, end_date.month)
    df_2 = df_2[pd.to_datetime(df_2.tpep_dropoff_datetime) <= end_date]
    df_final = pd.concat([df_1, df_2])
    # in case the time_delta covers 3 months
    # TODO works for 45 days, but not for more than 3 months
    middle_month = start_date + relativedelta(months=1)
    if end_date.month != middle_month.month:
        df_3 = get_data(middle_month.year, middle_month.month)
        df_final = pd.concat([df_final, df_3])

    return df_final.trip_distance.mean()
