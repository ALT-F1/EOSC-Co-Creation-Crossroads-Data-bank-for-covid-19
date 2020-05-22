import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import calendar
import datetime
from openweathermap_json_to_csv import json_str_to_flat_pd

secret_api_key = os.environ['OPENWEATHERMAP_API_KEY']

# %% [markdown]
# # Filter the list of cities in Belgium from OpenWeatherMap
# 

# %% [code]
# libraries initializations
import json

# variables initializations
history_city_list_path = os.path.join(os.path.abspath(os.getcwd()), "src", "data", "history.city.list.json") # source https://openweathermap.org/history
postal_codes_in_be_from_bpost_be_in_fr_path = os.path.join(os.path.abspath(os.getcwd()), "src", "data", "zipcodes_alpha_fr_new.csv") # source https://www.bpost.be/site/fr/envoyer/adressage/rechercher-un-code-postal
postal_codes_in_be_from_bpost_be_in_nl_path = os.path.join(os.path.abspath(os.getcwd()), "src", "data", "zipcodes_alpha_nl_new.csv") # source https://www.bpost.be/site/nl/verzenden/adressering/zoek-een-postcode

output_directory = os.path.join(os.path.abspath(os.getcwd()), "src", "data", "export_from_openweathermap", "historical")

# create directories
from pathlib import Path

Path(output_directory).mkdir(parents=True, exist_ok=True)



# %% [markdown]
# # Extract: Extract list of WW cities recognized by OpenWeatherMap

# %% [code]
# load the history city list
with open(history_city_list_path) as f: 
    d = json.load(f) 
    
df_weather_in_cities = pd.json_normalize(d)

# %% [markdown]
# # Transform: keep the Belgian cities only from the OpenWeatherMap' list

# %% [code]
# filter the belgian cities
df_cities_weather_in_be = df_weather_in_cities[df_weather_in_cities['city.country']=='BE'].copy(deep=True)


# %% [markdown]
# # Transform: column in lowercase

# %% [code]
# change column to lowercase
df_cities_weather_in_be['city.findname'] = df_cities_weather_in_be['city.findname'].str.lower()
df_cities_weather_in_be['city.name'] = df_cities_weather_in_be['city.name'].str.lower()

# %% [code]
df_cities_weather_in_be.shape

# %% [markdown]
# # Transform : Roeulx (OpenWeatherMap) -> Le Roeulx (bpost.be)

# %% [code]
df_cities_weather_in_be[df_cities_weather_in_be['city.name']=='roeulx'] = df_cities_weather_in_be[df_cities_weather_in_be['city.name']=='roeulx'].replace(['roeulx'], ['le roeulx'])

#= df_cities_weather_in_be[df_cities_weather_in_be['city.name']=='Roeulx']


# %% [markdown]
# # Transform: remove unnecessary columns and rename the column (city.id.$numberLong'->id)

# %% [code]
df_cities_weather_in_be=df_cities_weather_in_be.drop(columns=['id', 'city.zoom.$numberLong', 'city.coord.lon.$numberLong',
       'city.coord.lat.$numberLong', 'id.$numberLong'])

# %% [code]
# rename "city.id.$numberLong" in id
df_cities_weather_in_be=df_cities_weather_in_be.rename(columns={'city.id.$numberLong':'id'})

# %% [code]
df_cities_weather_in_be.columns

# %% [markdown]
# # Transform: OpenWeatherMap: round the longitude and latitude to match the lat and long from geonames.org

# %% [code]
# df_cities_weather_in_be['rounded_lat'] = df_cities_weather_in_be.loc[:,('city.coord.lat')].apply(lambda x: np.round(x, 4))#

# %% [code]
# df_cities_weather_in_be['rounded_lon'] = df_cities_weather_in_be['city.coord.lon'].apply(lambda x: np.round(x, 4))

# %% [code]
# check if the dtypes of longitude and latitude are float64
#df_cities_weather_in_be.dtypes

# %% [code]
df_cities_weather_in_be

# %% [markdown]
# # Extract: Extract the Belgian postal codes from the BPOST.BE database

# %% [code]
# source https://www.bpost.be/site/fr/envoyer/adressage/rechercher-un-code-postal
columns={'Postcode':'Code postal', 'Plaatsnaam':  'Localité', 'Deelgemeente' :'Sous-commune', 'Hoofdgemeente':'Commune principale', 'Provincie':'Province'}
postal_codes_in_be_from_bpost_be_in_fr = pd.read_csv(postal_codes_in_be_from_bpost_be_in_fr_path, sep=',', header=0)
postal_codes_in_be_from_bpost_be_in_nl = pd.read_csv(postal_codes_in_be_from_bpost_be_in_nl_path, sep=',', header=0)

# %% [code]
postal_codes_in_be_from_bpost_be_in_fr[postal_codes_in_be_from_bpost_be_in_fr['Commune principale']=="Zwijndrecht".upper()]

# %% [code]
postal_codes_in_be_from_bpost_be_in_nl=postal_codes_in_be_from_bpost_be_in_nl.rename(columns=columns, errors='raise')
postal_codes_in_be_from_bpost_be_in_nl.columns

# %% [code]
postal_codes_in_be_from_bpost_be_in_nl[postal_codes_in_be_from_bpost_be_in_nl['Commune principale']=="Zwijndrecht".upper()]

# %% [code]
df_postal_codes_in_be = pd.concat([postal_codes_in_be_from_bpost_be_in_nl, postal_codes_in_be_from_bpost_be_in_fr])
df_postal_codes_in_be.columns

# %% [code]
df_postal_codes_in_be.shape

# %% [markdown]
# # Transform: Reduce the amount of columns in final df_postal_codes_in_be

# %% [code]
#keep fewer columns
df_postal_codes_in_be = df_postal_codes_in_be[['Code postal', 'Commune principale', 'Localité']]

# %% [code]
df_postal_codes_in_be[df_postal_codes_in_be['Commune principale']=="Zwijndrecht".upper()]

# %% [markdown]
# # Transform: Add missing names in English

# %% [code]
# add missing cities
missing_english_cities = pd.DataFrame({"Code postal":[1000, 1342], 
                    "Localité":["Brussels", "Ottignies"],
                    "Commune principale":["Brussels", "Ottignies"]}) 
df_postal_codes_in_be=df_postal_codes_in_be.append(missing_english_cities)
df_postal_codes_in_be.shape

# %% [markdown]
# # Transform: change columns in lower case

# %% [code]
# change column to lowercase
df_postal_codes_in_be['Localité'] = df_postal_codes_in_be['Localité'].str.lower()
df_postal_codes_in_be['Commune principale'] = df_postal_codes_in_be['Commune principale'].str.lower()

# %% [markdown]
# # Transform: remove accents and apostophes and use 'normalized' columns

# %% [code]
import unidecode
from pandas.io.json import json_normalize
def remove_accents_apostrophe(a):
    a= unidecode.unidecode(a) #remove accent
    a= a.replace("'", '')  #remove apostrophe
    return a

# %% [code]
df_postal_codes_in_be['Commune principale normalized'] = df_postal_codes_in_be['Commune principale'].apply(remove_accents_apostrophe)

# %% [code]
df_postal_codes_in_be['Localité normalized'] = df_postal_codes_in_be['Localité'].apply(remove_accents_apostrophe)

# %% [code]
df_postal_codes_in_be

# %% [markdown]
# # Transform: drop all duplicates from df_postal_codes_in_be

# %% [code]
# drop duplicates and keep the fist one
df_postal_codes_in_be=df_postal_codes_in_be.drop_duplicates(keep='first')

# %% [markdown]
# # Helper: store dataframes in XLS files

# %% [code]
df_postal_codes_in_be['Commune principale'].to_excel(os.path.join(output_directory, "tmp_comm_princ.xlsx"))

# %% [code]
df_postal_codes_in_be['Commune principale normalized'].to_excel(os.path.join(output_directory, "tmp_com_princ_norm.xlsx"))

# %% [code]
df_postal_codes_in_be.to_excel(os.path.join(output_directory, "df_postal_codes_in_be.xlsx"))

# %% [code]
df_cities_weather_in_be.to_excel(os.path.join(output_directory, "df_cities_weather_in_be.xlsx"))

# %% [markdown]
# # Transform: Merge OpenWeatherMap and BPOST.BE datasets

# %% [markdown]
# # Transform: merge df_postal_codes_in_be, df_cities_weather_in_be, how='right'

# %% [code]
merged_right = pd.merge(df_postal_codes_in_be, df_cities_weather_in_be, how='right', left_on=['Commune principale normalized'], right_on=['city.findname'], validate='many_to_one')

# %% [code]
merged_right.dtypes

# %% [code]
merged_right.shape

# %% [code]
merged_right

# %% [code]
df_postal_codes_in_be[df_postal_codes_in_be['Commune principale normalized']=="zwijndrecht"]

# %% [code]
merged_right[merged_right['city.name']=="zwijndrecht"]

# %% [code]
merged_right[merged_right['city.name']=="brussels"]

# %% [code]
merged_right_localite = merged_right[merged_right['Code postal'].isna()].copy(deep=True)

# %% [code]
merged_right_localite.shape

# %% [code]
rows_to_remove_from_merged_right = merged_right.index[merged_right[merged_right['Code postal'].isna()].index]

# %% [code]
rows_to_remove_from_merged_right

# %% [code]
# remove the columns containing rows with empty 'Code postal' that will be updated in the coming lines
merged_right = merged_right.drop(rows_to_remove_from_merged_right)

# %% [code]
merged_right.shape

# %% [code]
merged_right_localite.columns

# %% [code]
# remove columns with 'code postal' containing null that will be injected in the following merge 
merged_right_localite=merged_right_localite.drop(columns=['Code postal', 'Commune principale', 'Localité','Commune principale normalized', 'Localité normalized'])

# %% [code]
merged_right_localite.to_excel(os.path.join(output_directory, 'merged_right_localite.xlsx'))

# %% [code]
# Transform : Merge localité and city.findname IF code postal is NaN
merged_right_localite_new = pd.merge(df_postal_codes_in_be, merged_right_localite, how='right', left_on=['Localité normalized'], right_on=['city.findname'], validate='many_to_one')

# %% [code]
merged_right_localite_new.shape

# %% [markdown]
# # Tranform : Merge localité and city.findname IF code postal is NaN

# %% [code]
merged_right_localite_new

# %% [code]
merged_right[merged_right['city.name'] == 'puurs']

# %% [code]
df_final = pd.concat([merged_right_localite_new, merged_right]).sort_values('Code postal')

# %% [code]
df_final

# %% [code]
# caveat: change the format of the 'Code postal' to int because pandas changes it into a float after the merge
df_final = df_final.where(pd.notnull(df_final), 0)
df_final['Code postal'] = df_final['Code postal'].astype(int)

# %% [code]
df_final.to_excel(os.path.join(output_directory, "df_final.xlsx"))

# %% [code]
# drop duplicated bpost.be 'Code postal'

# %% [code]
df_final_drop_duplicates = df_final.drop_duplicates(subset=['Code postal'], keep='first')

# %% [code]
df_final_drop_duplicates.to_excel(os.path.join(output_directory, 'df_final_drop_duplicates.xlsx'))

# %% [markdown]
# # load !!!!

# %% [markdown]
# 

# %% [markdown]
# # Load : get the weather of today for the first item

# %% [code]
def openweatermap_get_history(city_id, start,end):
    import http.client
    import mimetypes
    conn = http.client.HTTPSConnection("history.openweathermap.org")
    payload = ''
    headers = {}
    conn.request("GET", f"/data/2.5/history/city?id={city_id}&start={start}&end={end}&appid={secret_api_key}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    result = data.decode("utf-8")
    # print(result)
    return result

# %% [code]
def get_range_in_a_month(year, month, current_week, days_in_a_week, days_in_current_month):
   
    start_datetime = datetime.datetime(year=year, month=month, day=1+(current_week*days_in_a_week), hour=0, minute=0)
    printable_start_datetime = start_datetime.strftime("%Y-%m-%d_%Hh%M")
    
    end_day = days_in_current_month if 7+(current_week*days_in_a_week)>days_in_current_month else 7+(current_week*days_in_a_week)
    
    end_datetime = datetime.datetime(year=year, month=month, day=end_day, hour=23, minute=0)
    printable_end_datetime = end_datetime.strftime("%Y-%m-%d_%Hh%M")
    
    print(f"{printable_start_datetime}, {printable_end_datetime}")

    return start_datetime, end_datetime


def get_first_and_last_day_of_the_month(year, month):
   
    first_day_datetime = datetime.datetime(year=year, month=month, day=1, hour=0, minute=0)
    printable_start_datetime = first_day_datetime.strftime("%Y-%m-%d_%Hh%M")
      
    last_day_datetime = datetime.datetime(year=year, month=month, day=calendar.monthrange(year,month)[1], hour=23, minute=0)
    printable_last_datetime = last_day_datetime.strftime("%Y-%m-%d_%Hh%M")
    
    print(f"{printable_start_datetime}, {printable_last_datetime}")

    return first_day_datetime, last_day_datetime

# %% [markdown]
# # Store : save one file per week per postal code
# 0612_saint-nicolas_from_2020-05-29_00h00_to_2020-05-31_23h00
    
# %% [code]

def save_to_file(current_row, year=2020, months=[3,4,5], format='csv'):
    
    city_name = current_row['city.findname']

    
    city_id = current_row['id']
    city_postal_code = str(current_row['Code postal'])
    
    days_in_a_week= 7
    df_csv = pd.DataFrame()
    print(f"save : {city_postal_code.zfill(4)}-{city_name}")
    first_day_of_the_month, last_day_of_the_month = get_first_and_last_day_of_the_month(year=year, month=months[len(months)-1])
    for month in months:
        days_in_current_month = calendar.monthrange(year,month)[1]
        for current_week in range(0,((days_in_current_month)//7)+1):
            start_datetime, end_datetime = get_range_in_a_month(year, month, current_week, days_in_a_week, days_in_current_month)

            #save_weather
            weather_json = openweatermap_get_history(city_id, start_datetime.strftime('%s'), end_datetime.strftime('%s'))

            filename = os.path.join(output_directory, f'{city_postal_code.zfill(4)}_{city_name}_from_{start_datetime.strftime("%Y-%m-%d_%Hh%M")}_to_{end_datetime.strftime("%Y-%m-%d_%Hh%M")}-{start_datetime.strftime("%s")}_to_{end_datetime.strftime("%s")}')
            
            if format=='csv':
                df_csv = pd.concat([df_csv, json_str_to_flat_pd(weather_json)])

            elif format=='json':
                with open(f"{filename}.json", 'w') as outfile:
                    json.dump(weather_json, outfile, indent=2)

    if format=='csv':
        filename = os.path.join(output_directory, f'{city_postal_code.zfill(4)}_{city_name}_from_{first_day_of_the_month.strftime("%Y-%m-%d_%Hh%M")}_to_{last_day_of_the_month.strftime("%Y-%m-%d_%Hh%M")}-{first_day_of_the_month.strftime("%s")}_to_{last_day_of_the_month.strftime("%s")}')
        df_csv.to_csv(f"{filename}.csv", index=False)

if __name__ == "__main__":
    df_final_drop_duplicates.apply(save_to_file, axis=1, args=[2020, [3,4,5], 'csv'])
