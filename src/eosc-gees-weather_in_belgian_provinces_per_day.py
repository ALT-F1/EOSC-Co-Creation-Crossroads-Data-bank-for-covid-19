# %% [markdown]
# # Objective
#
# Is it realistic to have a daily update and to keep the up-to-date file always at the same web address (so that I can wget it automatically)?
#
# ****
# by_province_daily_reports/YYY-MM-DD.csv
#

# %% [code]
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import threading
from datetime import datetime, timedelta, date
import json
#from altf1be_helpers import output_directory, daterange
from altf1be_helpers import AltF1BeHelpers
from bpost_be_postal_code_helpers import BPost_postal_codes
from openweathermap_helpers import OpenWeatherMap
import mimetypes
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
from time import perf_counter
import time
import re
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

# %% [code]
# keep: import libraries

FILE_ALREADY_EXISTS = 1


class BelgianCities():

    def __init__(self):
        self.altF1BeHelpers = AltF1BeHelpers()

        # %% [code]
        # keep: get Belgian Postal codes
        self.bpost_postal_codes = BPost_postal_codes()
        print(self.bpost_postal_codes.df_postal_codes_in_be)

        # %% [code]
        # keep: get Belgian cities from OpenWeatherMap
        self.openWeatherMap = OpenWeatherMap()
        self.openWeatherMap.build_df()
        print(self.openWeatherMap.df_cities_weather_in_be)

    def thread_save(self, single_date):
        self.df_merged.apply(
            belgianCities.save_to_file, axis=1, args=[single_date.year, single_date.month, single_date.day, 'csv'])

    def save_from_to_date(self, start_date=None, end_date=None):
        if start_date is None:
            # set start_date to 2 days before to ensure that the weather data exist for 24 hours
            start_date = datetime.now() - timedelta(1)

        if end_date is None:
            # set end_date to yesterday to ensure that the weather data exist for 24 hours
            end_date = datetime.now() - timedelta(0)

        list_threads = []
        # see https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
        for single_date in self.altF1BeHelpers.daterange(start_date, end_date):
            x = threading.Thread(target=self.thread_save, args=(single_date,))
            list_threads.append(x)
            x.start()

        print(f"All threads are started: {len(list_threads)}")

        for t in list_threads:
            t.join()  # Wait until thread terminates its task

    def save_to_file(self, current_row, year=2020, month=5, day=1, format='csv'):
        """
            get the weather for a specific day for from OpenWeatherMap.org
        """

        city_name = current_row['city.findname']
        city_id = current_row['id']
        city_postal_code = str(current_row['Code postal'])

        start_datetime, end_datetime = self.openWeatherMap.get_range_between_days(
            year, month, day)

        filename = os.path.join(self.altF1BeHelpers.output_directory(['by_date', start_datetime.strftime("%Y-%m-%d")]),
                                f'{city_postal_code.zfill(4)}-{city_name}-{start_datetime.strftime("%Y-%m-%d")}')

        if os.path.exists(f"{filename}.json"):
            print(
                f"WARNING: File already exists: We skip its retrieval from OpenWeathMap.org: {filename}.json")
            with open(f"{filename}.json") as json_file:
                weather_json = json.load(json_file)
            return weather_json

        print(f"File stored in : {os.path.dirname(filename)}")

        # get the weather from OpenWeatherMap.org
        weather_json = self.openWeatherMap.get_history(
            city_id, start_datetime.strftime('%s'), end_datetime.strftime('%s'))

        df_csv = pd.DataFrame()
        if format == 'csv':
            df_csv = pd.concat(
                [df_csv, self.openWeatherMap.json_str_to_flat_df(weather_json)])

            df_csv.to_csv(f"{filename}.csv", index=False)
            print(f"File stored in : {filename}.csv")

        with open(f"{filename}.json", 'w') as outfile:
            json.dump(weather_json, outfile, indent=2)
            print(f"File stored in : {filename}.json")

        return weather_json

    def merge_openweathermap_bpost(self):
        """
        Merge OpenWeatherMap.org and BPost.be cities list and postal codes respectivelly. 
        """

        # %% [code]
        # Transform: merge df_postal_codes_in_be, df_cities_weather_in_be, how='right'"
        merged_right = pd.merge(self.bpost_postal_codes.df_postal_codes_in_be, self.openWeatherMap.df_cities_weather_in_be, how='right', left_on=[
                                'Localité normalized'], right_on=['city.findname'], validate='many_to_one')

        # Find Belgian localité that did not find a Postal code : knokke-heist, chasse royale, plombieres, cureghem, brunehault
        merged_right_localite = merged_right[merged_right['Code postal'].isna()].copy(
            deep=True)
        if (merged_right_localite.shape[0] > 0):
            print(
                f"WARNING: They are {merged_right_localite.shape[0]} city.name(s) inside OpenWeatherMap.org db that do not match BPost.be 'Localité'")
            print(f"ACTION: Add the 'Localité' inside the variable BPost_postal_codes.missing_english_cities and run the code again")
            print(merged_right_localite)

            # The system tries to find missing 'localité' by looking at

            # We need to remove the missing Localité from the df containing the merge between OpenWeatherMap and BPost postal codes
            rows_to_remove_from_merged_right = merged_right.index[merged_right[merged_right['Code postal'].isna(
            )].index]

            # remove the columns containing rows with empty 'Code postal' that will be updated in the coming lines
            merged_right = merged_right.drop(rows_to_remove_from_merged_right)

            # remove columns with 'code postal' containing null that will be injected in the following merge
            merged_right_localite = merged_right_localite.drop(
                columns=['Province', 'Code postal', 'Commune principale', 'Localité', 'Commune principale normalized', 'Localité normalized'])

            # Transform : Merge localité and city.findname IF code postal is NaN
            merged_right_localite = pd.merge(
                self.bpost_postal_codes.df_postal_codes_in_be,
                merged_right_localite,
                how='right',
                left_on=['Commune principale normalized'],
                right_on=['city.findname'],
                validate='many_to_one'
            )

        self.df_merged = pd.concat(
            [merged_right_localite, merged_right]).sort_values('Code postal')

        # caveat: change the format of the 'Code postal' to int because pandas changes it into a float after the merge
        self.df_merged = self.df_merged.where(pd.notnull(self.df_merged), 0)
        self.df_merged['Code postal'] = self.df_merged['Code postal'].astype(
            int)

        # drop duplicated bpost.be 'Code postal'
        self.df_merged = self.df_merged.drop_duplicates(
            subset=['Code postal'], keep='first')

        return self.df_merged

    def build_df_per_province_per_quartile(self):
        """Build a DataFrame of BPost.be data grouped by province and per quartile (25, 50 and 75) 

        """
        self.bpost_postal_codes.df_postal_codes_in_be = self.bpost_postal_codes.translate_provinces_in_french(
            self.bpost_postal_codes.df_postal_codes_in_be)
        return self.bpost_postal_codes.df_postal_codes_in_be.groupby(['Province'])[
            'Code postal'].apply(set)

    def append_df_per_province(self, df, filename):
        """
        Use the postal code of the filename to append in a DataFrame the province, the postal code and the Date in YYY-MM-DD format

        Returns
        -------
        DataFrame
            DataFrame appended with Three columns : Province, Postal code and date

        """
        postal_code = filename[:4]
        province = self.bpost_postal_codes.get_province_from(postal_code=int(
            postal_code), df=self.bpost_postal_codes_grouped_by_province)
        df['Province'] = province
        df['Postal code'] = postal_code
        df['date'] = df['dt'].apply(
            lambda x: time.strftime('%Y-%m-%d', time.localtime(x)))
        # print(f"{postal_code}-{province}")
        # print(df)
        # df.columns
        #current_province = df_postal_codes_in_be.loc[df_postal_codes_in_be['Code postal'] == df.loc['Province']]
        return df

    def add_quantiles(self, df):
        # per province
        columns = [
            'message',
            'cod',
            'dt',
            'Province',
            'date',
            'main.temp25', 'main.temp50', 'main.temp75',
            'main.feels_like25', 'main.feels_like50', 'main.feels_like75',
            'main.pressure25', 'main.pressure50', 'main.pressure75',
            'main.humidity25', 'main.humidity50', 'main.humidity75',
            'main.temp_min25', 'main.temp_min50', 'main.temp_min75',
            'main.temp_max25', 'main.temp_max50', 'main.temp_max75',
            'wind.speed25', 'wind.speed50', 'wind.speed75',
            'wind.deg25', 'wind.deg50', 'wind.deg75',
        ]
        df_quantiles = pd.DataFrame(columns=columns)
        #lines = 0

        df_quantiles_sorted = df.sort_values(
            ['Province', 'dt']).copy(deep=True)

        for province in df_quantiles_sorted['Province'].unique():
            # per day
            # print(f"PROVINCE: {province}")
            for date in df_quantiles_sorted['date'].unique():
                # print(f"LINES: {lines} - {df_quantiles.shape}")
                #lines = lines+1
                # print(f"DATE : {date}")
                # compute quantile
                current_date_df = df_quantiles_sorted.loc[
                    (df_quantiles_sorted['Province'] == province) & (
                        df_quantiles_sorted['date'] == date)
                ]

                new_row = pd.DataFrame(
                    [
                        [
                            current_date_df.iloc[0]['message'],
                            current_date_df.iloc[0]['cod'],
                            current_date_df.iloc[0]['dt'],
                            province,
                            date,
                            current_date_df['main.temp'].quantile(.25),
                            current_date_df['main.temp'].quantile(.50),
                            current_date_df['main.temp'].quantile(.75),
                            current_date_df['main.feels_like'].quantile(.25),
                            current_date_df['main.feels_like'].quantile(.50),
                            current_date_df['main.feels_like'].quantile(.75),
                            current_date_df['main.pressure'].quantile(.25),
                            current_date_df['main.pressure'].quantile(.50),
                            current_date_df['main.pressure'].quantile(.75),
                            current_date_df['main.humidity'].quantile(.25),
                            current_date_df['main.humidity'].quantile(.50),
                            current_date_df['main.humidity'].quantile(.75),
                            current_date_df['main.temp_min'].quantile(.25),
                            current_date_df['main.temp_min'].quantile(.50),
                            current_date_df['main.temp_min'].quantile(.75),
                            current_date_df['main.temp_max'].quantile(.25),
                            current_date_df['main.temp_max'].quantile(.50),
                            current_date_df['main.temp_max'].quantile(.75),
                            current_date_df['wind.speed'].quantile(.25),
                            current_date_df['wind.speed'].quantile(.50),
                            current_date_df['wind.speed'].quantile(.75),
                            current_date_df['wind.deg'].quantile(.25),
                            current_date_df['wind.deg'].quantile(.50),
                            current_date_df['wind.deg'].quantile(.75)
                        ]
                    ],
                    columns=columns)

                #new_row = pd.DataFrame([date], columns=['message'])
                print(f"add_quantiles: new_row.shape : {new_row.shape}")
                # print(f"new_row : {new_row}")
                #print(f"new_row.columns : {new_row.columns}")
                df_quantiles = df_quantiles.append(new_row, ignore_index=True)
        return df_quantiles

    def thread_save_quantiles(self, dirname, filenames):
        index = 0
        df_provinces_collection = pd.DataFrame()  # one dataframe per province
        directory_by_date = os.path.basename(os.path.normpath(dirname))
        mat = re.match('(\d{4})[/.-](\d{2})[/.-](\d{2})$',
                       directory_by_date)
        if mat is None:
            print(
                f"{directory_by_date} DOES NOT match a date, we skip the directory")
        else:
            filename_with_collection = os.path.join(
                self.altF1BeHelpers.output_directory(
                    ['by_province_and_quartile']
                ),
                f"{directory_by_date}.csv")

            if os.path.exists(filename_with_collection):
                print(
                    f"WARNING: File already exists: We skip the grouping by province: {filename_with_collection}")
            else:
                for filename in filenames:
                    if filename.endswith('.csv'):
                        csv_path = os.path.join(dirname, filename)
                        print(
                            f"loading: {index}/{len(filenames)} - {csv_path}"
                        )
                        df_provinces_collection = pd.concat(
                            [
                                df_provinces_collection,
                                self.append_df_per_province(
                                    pd.read_csv(csv_path, sep=','), filename
                                )
                            ]
                        )
                    index = index+1

                df_quantiles = self.add_quantiles(df_provinces_collection)

                # store current dataframe containing the weather of all cities from March 01 to May 22, 2020
                df_quantiles.to_csv(
                    f"{filename_with_collection}")

                # df_quantiles.to_pickle(f"{output_filename_with_collection}.pkl")

                print(
                    f"DataFrame grouped by province and quartile are stored here : {filename_with_collection}")

            df_provinces_collection = pd.DataFrame()

    def create_files_grouped_by_province_with_quartiles(self):
        """Create one file per day containing the weather data including the province and the quartiles for the temperature, the humidity and the wind

        """
        t1_start = perf_counter()

        self.bpost_postal_codes_grouped_by_province = self.build_df_per_province_per_quartile()
        openweathermap_org_weather_by_date_directory = self.altF1BeHelpers.output_directory([
                                                                                            'by_date'])

        print(
            f"openweathermap_org_weather_by_date_directory: {openweathermap_org_weather_by_date_directory}")

        list_threads = []

        for dirname, _, filenames in os.walk(openweathermap_org_weather_by_date_directory):
            x = threading.Thread(
                target=self.thread_save_quantiles, args=(dirname, filenames))
            list_threads.append(x)
            x.start()

        print(f"All threads are started: {len(list_threads)}")

        for t in list_threads:
            t.join()  # Wait until thread terminates its task

        t1_stop = perf_counter()

        print("Elapsed time:", t1_stop, t1_start)

        print("Elapsed time during the whole program in seconds:",
              t1_stop-t1_start)

        # %% [code]

    def create_df_with_grouped_by_province_with_quartiles(self):
        """Create one file containing all weather data stored in output_directory/data/by_date

        """
        t1_start = perf_counter()
        df_grouped_by_province_with_quartiles = pd.DataFrame()

        openweathermap_org_weather_by_date_directory = self.altF1BeHelpers.output_directory(
            ['by_province_and_quartile']
        )
        print(
            f"openweathermap_org_weather_by_date_directory: {openweathermap_org_weather_by_date_directory}"
        )
        filename_with_collection = os.path.join(
            self.altF1BeHelpers.output_directory(
                ['latest']
            ),
            f"by_province_and_quartile.csv")
        index = 0
        for dirname, _, filenames in os.walk(openweathermap_org_weather_by_date_directory):
            for filename in filenames:
                if filename.endswith('.csv'):
                    csv_path = os.path.join(dirname, filename)
                    print(
                        f"loading: {index}/{len(filenames)} - {csv_path}"
                    )
                    df_grouped_by_province_with_quartiles = pd.concat(
                        [
                            df_grouped_by_province_with_quartiles,
                            pd.read_csv(csv_path, sep=',')
                        ]
                    )
                index = index+1

        # store current dataframe containing the weather
        df_grouped_by_province_with_quartiles.to_csv(
            f"{filename_with_collection}")

        print(
            f"DataFrame grouped by province and quartile are stored here : {filename_with_collection}")

        t1_stop = perf_counter()

        print("Elapsed time:", t1_stop, t1_start)

        print("create_df_with_grouped_by_province_with_quartiles: Elapsed time during the whole program in seconds:",
              t1_stop-t1_start)


def test_save_json_csv_from_openweathermap(belgianCities):
    merged_df = belgianCities.merge_openweathermap_bpost()
    print(f"belgianCities.merge_openweathermap_bpost: {merged_df}")

    # save the weather of all Belgian cities of yesterday (default behavior)
    # belgianCities.save_from_to_date()
    belgianCities.save_from_to_date(start_date=datetime(2020, 6, 1)) # store the weather data for a specific date
    # belgianCities.save_from_to_date(start_date=datetime(2020, 3, 1), end_date=datetime(2020, 3, 31)) # store the weather data for and to a certain date


def test_create_files_by_provinces_and_quartiles(belgianCities):
    belgianCities.create_files_grouped_by_province_with_quartiles()


def test_create_df_with_grouped_by_province_with_quartiles(belgianCities):
    belgianCities.create_df_with_grouped_by_province_with_quartiles()


if __name__ == "__main__":
    belgianCities = BelgianCities()

    test_save_json_csv_from_openweathermap(belgianCities)
    test_create_files_by_provinces_and_quartiles(belgianCities)
    test_create_df_with_grouped_by_province_with_quartiles(belgianCities)
