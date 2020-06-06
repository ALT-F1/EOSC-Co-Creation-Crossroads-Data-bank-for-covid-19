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

from datetime import datetime, timedelta, date
import json
from altf1be_helpers import output_directory, daterange
from bpost_be_postal_code import BPost_postal_codes
from openweathermap_helpers import OpenWeatherMap
import http.client
import mimetypes
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

# %% [code]
# keep: import libraries

FILE_ALREADY_EXISTS = 1
import threading


class BelgianCities():

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

        # see https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
        for single_date in daterange(start_date, end_date):
            x = threading.Thread(target=self.thread_save, args=(single_date,))
            x.start()
            

    def save_to_file(self, current_row, year=2020, month=5, day=1, format='csv'):
        """
            get the weather for a specific day for from OpenWeatherMap.org
        """

        city_name = current_row['city.findname']
        city_id = current_row['id']
        city_postal_code = str(current_row['Code postal'])

        start_datetime, end_datetime = self.openWeatherMap.get_range_between_days(
            year, month, day)

        filename = os.path.join(output_directory([start_datetime.strftime("%Y-%m-%d")]),
                                f'{city_postal_code.zfill(4)}-{city_name}-{start_datetime.strftime("%Y-%m-%d")}')
        
        if os.path.exists(f"{filename}.json"):
            print(
                f"File already exists: We skip its retrieval from OpenWeathMap.org: {filename}.json")
            with open(f"{filename}.json") as json_file:
                weather_json = json.load(json_file)
            return weather_json

        print(f"File stored in : {os.path.dirname(filename)}")

        # get the weather from OpenWeatherMap.org
        weather_json = self.openweatermap_get_history(
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

    def openweatermap_get_history(self, city_id, start, end):

        conn = http.client.HTTPSConnection("history.openweathermap.org")
        payload = ''
        headers = {}
        conn.request(
            "GET", f"/data/2.5/history/city?id={city_id}&start={start}&end={end}&appid={self.openWeatherMap.secret_api_key}", payload, headers)
        res = conn.getresponse()
        data = res.read()
        result = data.decode("utf-8")
        # print(result)
        return result

    def merge_openweathermap_bpost(self):
        """
        Merge OpenWeatherMap.org and BPost.be cities list and postal codes respectivelly. 
        """
        # %% [code]
        # keep: get Belgian cities from OpenWeatherMap
        self.openWeatherMap = OpenWeatherMap()
        print(self.openWeatherMap.df_cities_weather_in_be)

        # %% [code]
        # keep: get Belgian Postal codes
        bpost_postal_codes = BPost_postal_codes()
        print(bpost_postal_codes.df_postal_codes_in_be)

        # %% [code]
        # Transform: merge df_postal_codes_in_be, df_cities_weather_in_be, how='right'"
        merged_right = pd.merge(bpost_postal_codes.df_postal_codes_in_be, self.openWeatherMap.df_cities_weather_in_be, how='right', left_on=[
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
            merged_right_localite = pd.merge(bpost_postal_codes.df_postal_codes_in_be, merged_right_localite, how='right', left_on=[
                                             'Commune principale normalized'], right_on=['city.findname'], validate='many_to_one')

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
        # %% [code]


if __name__ == "__main__":
    belgianCities = BelgianCities()
    merged_df = belgianCities.merge_openweathermap_bpost()
    print(f"belgianCities.merge_openweathermap_bpost: {merged_df}")
    belgianCities.save_from_to_date() # save the weather of all Belgian cities of yesterday by default 
    #belgianCities.save_from_to_date(start_date=datetime(2020, 3, 1))
