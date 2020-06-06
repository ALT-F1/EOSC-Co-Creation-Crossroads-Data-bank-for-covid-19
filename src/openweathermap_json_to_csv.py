import sys
import json
import pandas as pd
import openweathermap_error_codes as error_codes

json_file_path = "/home/abdelkrim/dev/github/OpenWeatherMap/src/data/export_from_openweathermap/historical/2020-03_March/1000_brussels_from_2020-03-01_00h00_to_2020-03-07_23h00-1583017200_to_1583618400.json"


def csv_to_df(json_data):
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
        if json_data["code"] == error_codes.DATA_FROM_FUTURE_IS_UNAVAILABLE:
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


def json_file_to_flat_pd():
    with open(json_file_path) as json_file:
        data = json.load(json_file)
        # print(data)
        j = json.loads(data)
        # print(j)
        df_csv = csv_to_df(j)

    return df_csv


def json_str_to_flat_pd(data):
    j = json.loads(data)
    df_csv = csv_to_df(j)
    return df_csv


def save_csv(df):
    df.to_csv("export_openweathermap.csv")


if __name__ == "__main__":
    print("do not this code")
    save_csv(json_file_to_flat_pd())
