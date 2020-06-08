# %% [code]
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

# initialize libraries
import http.client
import datetime
import json
from altf1be_helpers import AltF1BeHelpers
from os import path
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
import sys
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

# %% [code]

# initialize constants
DATA_FROM_FUTURE_IS_UNAVAILABLE = 400000


class OpenWeatherMap():
    """The class provides a read-to-use OpenWeatherMap functionalities 

    """

    def get_history(self, city_id, start, end):
        """Download the weather data from OpenWeatherMap.org

        See https://openweathermap.org/history

        Parameters
        ----------
        city_id : int
            The city id recognized by OpenWeatherMap.org
        start : start date (unix time, UTC time zone), e.g. start=1369728000
        end : end date (unix time, UTC time zone), e.g. end=1369789200

        Returns
        -------
        json string
            json string containing the weather for a specific date

        """
        conn = http.client.HTTPSConnection("history.openweathermap.org")
        payload = ''
        headers = {}
        conn.request(
            "GET", f"/data/2.5/history/city?id={city_id}&start={start}&end={end}&appid={self.secret_api_key}", payload, headers)
        res = conn.getresponse()
        data = res.read()
        result = data.decode("utf-8")
        # print(result)
        return result

    def save_to_file(self, current_row, year=2020, month=5, day=1, format='csv'):
        """Get the weather for a specific day for from OpenWeatherMap.org

        """

        city_name = current_row['city.findname']
        city_id = current_row['id']

        start_datetime, end_datetime = self.get_range_between_days(
            year, month, day)

        filename = os.path.join(
            self.altF1BeHelpers.output_directory(
                ['OpenWeatherMap.org', start_datetime.strftime("%Y-%m-%d")]
            ),
            f'{city_name}-{start_datetime.strftime("%Y-%m-%d")}'
        )

        if os.path.exists(f"{filename}.json"):
            print(
                f"File already exists: We skip its retrieval from OpenWeathMap.org: {filename}.json")
            with open(f"{filename}.json") as json_file:
                weather_json = json.load(json_file)
            return weather_json

        print(f"File stored in : {os.path.dirname(filename)}")

        # get the weather from OpenWeatherMap.org
        weather_json = self.get_history(
            city_id, start_datetime.strftime('%s'), end_datetime.strftime('%s'))

        df_csv = pd.DataFrame()
        if format == 'csv':
            df_csv = pd.concat(
                [df_csv, self.json_str_to_flat_df(weather_json)])

            df_csv.to_csv(f"{filename}.csv", index=False)
            print(f"File stored in : {filename}.csv")

        with open(f"{filename}.json", 'w') as outfile:
            json.dump(weather_json, outfile, indent=2)
            print(f"File stored in : {filename}.json")

        return weather_json

    def csv_to_df(self, json_data):
        """Convert a CSV into a Dataframe

        """
        # {'code': 400000, 'message': 'data from future is...available'}
        df_csv = pd.DataFrame(columns=['message',
                                       'cod',
                                       'city_id',
                                       'calctime',
                                       'cnt',
                                       'dt',
                                       'main.temp',
                                       'main.feels_like',
                                       'main.pressure',
                                       'main.humidity',
                                       'main.temp_min',
                                       'main.temp_max',
                                       'wind.speed',
                                       'wind.deg',
                                       'clouds.all',
                                       'weather.id',
                                       'weather.main',
                                       'weather.description',
                                       'weather.icon', ])

        try:
            if json_data["code"] == DATA_FROM_FUTURE_IS_UNAVAILABLE:
                return df_csv
        except KeyError:
            # openweathermap sent a reponse including wheater data
            pass
        else:
            print("TODO: handle this error")
            print("json_data: {json_data}")
            print("Unexpected error:", sys.exc_info()[0])
            raise

        message = json_data["message"]
        cod = json_data["cod"]
        city_id = json_data['city_id']
        calctime = json_data["calctime"]
        cnt = json_data["cnt"]

        for p in json_data['list']:

            for weather in p["weather"]:

                df_new_row = pd.DataFrame({
                    'message': [message],
                    'cod': [cod],
                    'city_id': [city_id],
                    'calctime': [calctime],
                    'cnt': [cnt],

                    'dt': p["dt"],
                    'main.temp': p["main"]["temp"],
                    'main.feels_like': p["main"]["feels_like"],
                    'main.pressure': p["main"]["pressure"],
                    'main.humidity': p["main"]["humidity"],
                    'main.temp_min': p["main"]["temp_min"],
                    'main.temp_max': p["main"]["temp_max"],

                    'wind.speed': p["wind"]["speed"],
                    'wind.deg': p["wind"]["deg"],

                    'clouds.all': p["clouds"]["all"],

                    'weather.id': weather["id"],
                    'weather.main': weather["main"],
                    'weather.description': weather["description"],
                    'weather.icon': weather["icon"],
                })

            df_csv = df_csv.append(df_new_row, ignore_index=True)

        return df_csv

    def json_str_to_flat_df(self, json_str):
        """Convert a JSON string into a flat DataFrame

        """
        j = json.loads(json_str)
        df_csv = self.csv_to_df(j)
        return df_csv

    def get_range_between_days(self, year, month, day):
        """Get a range of dates between 2 dates

        Returns
        -------
        unix time, UTC time zone
            start_datetime e.g. end=1369789200
            end_datetime e.g. end=1369789200

        """

        start_datetime = datetime.datetime(
            year=year, month=month, day=day, hour=0, minute=0)
        printable_start_datetime = start_datetime.strftime("%Y-%m-%d_%Hh%M")

        end_datetime = datetime.datetime(
            year=year, month=month, day=day, hour=23, minute=0)
        printable_end_datetime = end_datetime.strftime("%Y-%m-%d_%Hh%M")

        print(f"{printable_start_datetime}, {printable_end_datetime}")

        return start_datetime, end_datetime

    def get_range_in_a_month(self, year, month, current_week, days_in_a_week, days_in_current_month):
        """
            get a range in a month 
        """
        start_datetime = datetime.datetime(
            year=year, month=month, day=1+(current_week*days_in_a_week), hour=0, minute=0)
        printable_start_datetime = start_datetime.strftime("%Y-%m-%d_%Hh%M")

        end_day = days_in_current_month if 7 + \
            (current_week*days_in_a_week) > days_in_current_month else 7+(current_week*days_in_a_week)

        end_datetime = datetime.datetime(
            year=year, month=month, day=end_day, hour=23, minute=0)
        printable_end_datetime = end_datetime.strftime("%Y-%m-%d_%Hh%M")

        print(f"{printable_start_datetime}, {printable_end_datetime}")

        return start_datetime, end_datetime

    def save(self):

        self.df_cities_weather_in_be.to_excel(os.path.join(
            self.altF1BeHelpers.output_directory(['OpenWeatherMap.org']), "df_cities_weather_in_be.xlsx"))

    def get_openweathermap_secret_key(self):
        self.secret_api_key = None
        # Set the api_key and the paths on a Kaggle
        try:
            from kaggle_secrets import UserSecretsClient
            user_secrets = UserSecretsClient()
            self.secret_api_key = user_secrets.get_secret("API_KEY")
            print(f"OpenWeatherMap.org secret key found inside the Kaggle secret keys")
        except KeyError:
            print("KeyError: the secret key does not exist on Kaggle")
            #print("(Un)expected error:", sys.exc_info()[0])
        except ModuleNotFoundError:
            print("INFO: you may not be running kaggle, the OpenWeaterMap.org API KEY will be collected from the environment variable")
            #print("(Un)expected error:", sys.exc_info()[0])

        # Set the api_key and the paths on a regular OS
        if (self.secret_api_key == None):
            try:
                self.secret_api_key = os.environ['OPENWEATHERMAP_API_KEY']
                print(
                    f"OpenWeatherMap.org secret key found inside the environment variable")
            except KeyError:
                print("INFO: OPENWEATHERMAP_API_KEY is not a environment variable")
                print("You may use Kaggle to run this code")
                print(
                    "Consider adding an environment variable if OpenWeatherMap.org triggers an error related to the API TOKEN")

        if (self.secret_api_key == None):
            print(
                f"ERROR: OpenWeatherMap.org secret was NOT found inside Kaggle nor the environment variables")

        return self.secret_api_key

    def get_openweathermap_paths(self):
        """
        initialize three paths history_city_list_path, postal_codes_in_be_from_geonames_org
        """
        history_city_list_path = "kaggle/input/historycitylistjson/history.city.list.json"
        if (self.altF1BeHelpers.is_interactive()):
            # source https://openweathermap.org/history
            self.history_city_list_path = f"/{history_city_list_path}"
        else:
            self.history_city_list_path = os.path.join(
                os.path.abspath(os.getcwd()),
                "src",
                history_city_list_path
            )

        print(f"history_city_list_path: {self.history_city_list_path}")

        return self.history_city_list_path

    def clean_columns(self, df):
        """

        """
        # Transform: remove unnecessary columns and rename the column (city.id.$numberLong'->id)
        df = df.drop(columns=[
            'id',
            'city.zoom.$numberLong',
            'city.coord.lon.$numberLong',
            'city.coord.lat.$numberLong',
            'id.$numberLong'
        ])

        # rename "city.id.$numberLong" in id
        df = df.rename(
            columns={'city.id.$numberLong': 'id'})

        return df

    def rename_cities(self, df):
        """
            Make changes in the name of the cities to match the data inside the bpost.be database
        """
        # Transform : Roeulx (OpenWeatherMap) -> Le Roeulx (bpost.be)
        df[df['city.name'] == 'roeulx'] = df[df['city.name']
                                             == 'roeulx'].replace(['roeulx'], ['le roeulx'])

        return df

    def columns_in_lowercase(self, df):
        """
        Transform: column in lowercase
        """
        df['city.findname'] = df['city.findname'].str.lower()
        df['city.name'] = df['city.name'].str.lower()
        return df

    def keep_belgian_cities(self, df):
        """
            Transform: keep the Belgian cities only from the OpenWeatherMap' list
        """
        # filter the belgian cities
        df_cities_weather_in_be = df[df['city.country'] == 'BE'].copy(
            deep=True)
        return df_cities_weather_in_be

    def extract_ww_cities(self):
        """
            extract cities from list of cities recognized by OpenWeatherMap.org
        """
        # load the history city list
        with open(self.history_city_list_path) as f:
            d = json.load(f)

        return pd.json_normalize(d)

    def build_df(self):
        """
            Build the DataFrame containing OpenWeatherMap ready to be manipulated
        """
        df_weather_in_cities = self.extract_ww_cities()
        self.df_cities_weather_in_be = self.keep_belgian_cities(
            df_weather_in_cities)
        self.df_cities_weather_in_be = self.columns_in_lowercase(
            self.df_cities_weather_in_be)
        self.df_cities_weather_in_be = self.rename_cities(
            self.df_cities_weather_in_be)
        self.df_cities_weather_in_be = self.clean_columns(
            self.df_cities_weather_in_be)
        self.save()

    def __init__(self):
        self.altF1BeHelpers = AltF1BeHelpers()
        self.get_openweathermap_secret_key()
        self.get_openweathermap_paths()


# %% [code]
if __name__ == "__main__":

    # instanciate OpenWeatherMap
    openWeatherMap = OpenWeatherMap()
    print(
        f"OpenWeatherMap.org secret_api_key: {(openWeatherMap.secret_api_key)}")
    openWeatherMap.build_df()
    print(openWeatherMap.df_cities_weather_in_be)

    # store the weather of all cities recoginzed by OpenWeatherMap.org in csv and a json formats
    openWeatherMap.df_cities_weather_in_be.apply(
        openWeatherMap.save_to_file, axis=1, args=[2020, 5, 1, 'csv'])
