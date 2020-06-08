# Belgian Weather per day per province by using OpenWeatherMap.org and BPost.be datasources

The software collects the Weather of the Belgian communes from the OpenWeatherMap database. See [https://www.openweathermap.org](https://www.openweathermap.org)

The weather data will be linked to other data to answer one question: "Does the usage of the Weather data influence (or not) the model forecasting the spread of the COVID-19?"

# How to build the DataFrame by using OpenWeatherMap.org and BPost.be databases?

1. Set the api_key from [https://home.openweathermap.org/api_keys](https://home.openweathermap.org/api_keys)
2. Install python requirements by running `pip install -r requirements.txt`
3. Run `python src/eosc-gees-weather_in_belgian_provinces_per_day.py`
4. Look in the `output_directory/data/` directory to manipulate .csv and .json files

# What are the data available?

* Look into the directory [export_directory/data/by_date/yyy-mm-dd](export_directory/data/by_date/yyy-mm-dd)/*.{json|csv}` containing OpenWeatherMap.org for Belgian cities

* Weather data is grouped by province and per day
* We have computed the quantiles 25-50-75 for the following weather conditions: 
    * main.feels_like: See [https://openweather.co.uk/blog/post/new-feels-temperature-openweather-apis](https://openweather.co.uk/blog/post/new-feels-temperature-openweather-apis)
    * main.humidity
    * main.pressure
    * main.temp_max: maximal temperature
    * main.temp_min: minimal temperature
    * main.temp: temperature
    * wind.deg
    * wind.speed

# The context

Given the consequences of the COVID-19 pandemic for public health, many stakeholders in public and private sectors engage in global efforts to treat and understand those exposed to the virus and to contain the outbreak.

Universities and private companies contribute to the analysis of data useful to forecast the spread of the "Severe Acute Respiratory Syndrome CoronaVirus 2" (SARS-CoV-2).

Those persons include researchers and consultants who share their analysis to the public administration and members of governments who will shape the rules and regulations describing how the citizens should behave during the pandemic.

# Why collecting the weather data?

In Belgium, the  Group of Experts for an Exit Strategy (GEES) drafts proposals to envisage a gradual deconfinement. The GEES supports the [Belgian Federal Government](https://www.belgium.be/en/about_belgium/government/federal_authorities/federal_government).

See also [https://www.info-coronavirus.be/en](https://www.info-coronavirus.be/en)

The GEES uses data from researchers, amongst others. Those researchers build models of the spread of the virus by using diverse data: mobility, health, beds in hospitals, fatalities, current regulation ...

One question remains: **does the usage of the Weather data influence (or not) the spread of the virus?**

One of those groups of researchers includes the [Machine Learning Group](https://mlg.ulb.ac.be) (MLG) from the [Université Libre de Bruxelles](https://www.ulb.be). The MLG supports the initiative by providing models made of Artificial Intelligence/Machine Learning algorithms. The models built by the MLG influence the Exit Strategy.

# Technical challenges

OpenWeatherMap does not store the Postal code of the communes in Belgium. The Belgian Post provides the Belgian postal codes in French and Dutch [https://www.bpost.be](https://www.bpost.be)

This project joins both databases to enable a link between diverse types of data: mobility, postal codes, etc.

# The tools used to build the software

* Pandas [https://pandas.pydata.org](https://pandas.pydata.org)
* Python [https://www.python.org](https://www.python.org)
* Numpy [https://numpy.org](https://numpy.org)
* Kaggle [https://www.kaggle.com](https://www.kaggle.com)
* Visual Studio Code [https://code.visualstudio.com](https://code.visualstudio.com)

# The sponsors of the project

The **EOSC Secretariat** supports the governance of the **E**uropean **O**pen **S**cience **C**loud (EOSC). See [https://www.eoscsecretariat.eu/](https://www.eoscsecretariat.eu)

The EOSC supports projects aiming to make data **F**indable, **A**ccessible, **I**nteroperable, and **R**eproducible (FAIR) for scientists; these combinations would lead to (unforeseen) reuse and faster development of science. 

EOSC Secretariat granted funds to [http://www.alt-f1.be](http://www.alt-f1.be) to create a "Crossroads Data Bank for COVID-19".

Latest news from the European Commission: [https://ec.europa.eu/research/openscience/index.cfm?pg=open-science-cloud](https://ec.europa.eu/research/openscience/index.cfm?pg=open-science-cloud) 

**OpenWeatherMap** provides, free-of-charge, access to weather data to its historical weather data [https://openweathermap.org/api](https://openweathermap.org/api)

OpenWeather Ltd is a British-based tech company that provides weather and satellite data worldwide. OpenWeather collects and processes raw data from a variety of sources, and gives its customers access to the archive. See [https://openweathermap.org/](https://openweathermap.org/)

See [Openweather LTD Helps The Fight To Overcome COVID-19](https://bit.ly/2ZohgFF)

# The supporters of the project

**The Machine Learning Group**, founded in 2004 by [Gianluca Bontempi](https://mlg.ulb.ac.be/wordpress/members-2/gianluca-bontempi),  is a research unit of the Computer Science Department of the ULB (Université Libre de Bruxelles, Brussels, Belgium), Faculty of Sciences, currently co-headed by Prof. Gianluca Bontempi and Prof. [Tom Lenaerts](https://mlg.ulb.ac.be/wordpress/members-2/tom-lenaerts).

MLG targets machine learning and behavioral intelligence research focusing on time series analysis, big data mining, causal inference, network inference, decision-making models, and behavioral analysis with applications in data science, medicine, molecular biology, cybersecurity and social dynamics related to cooperation, emotions, and others.

See [https://mlg.ulb.ac.be/](https://mlg.ulb.ac.be/)

# Legal matters

The current software digests data that do not contain personal data.

The output of this project is linked to data that do not contain Personally Identifiable Information (PII). See [https://en.wikipedia.org/wiki/Personal_data](https://en.wikipedia.org/wiki/Personal_data)

# the data models

## Belgian Postal Codes

* Postal codes in French [https://www.bpost.be/site/fr/envoyer/adressage/rechercher-un-code-postal](https://www.bpost.be/site/fr/envoyer/adressage/rechercher-un-code-postal/)
* Postal codes in Dutch [https://www.bpost.be/site/nl/verzenden/adressering/zoek-een-postcode](https://www.bpost.be/site/nl/verzenden/adressering/zoek-een-postcode)

Here are the columns describing the postal codes: 

```
Index(['country code', 'postal code', 'place name', 'admin name1',
       'admin code1', 'admin name2', 'admin code2', 'admin name3',
       'admin code3', 'rounded_lat', 'rounded_lon', 'accuracy'],
      dtype='object')
```

## OpenWeatherMap List of cities IDs

Here are the columns describing the cities for which OpenWeatherMap tracks the Weather: [http://bulk.openweathermap.org/sample/history.city.list.json.gz](http://bulk.openweathermap.org/sample/history.city.list.json.gz)

```
Index(['id', 'city.id.$numberLong', 'city.name', 'city.findname',
       'city.country', 'city.coord.lon', 'city.coord.lat',
       'city.zoom.$numberLong', 'id.$numberLong', 'city.coord.lon.$numberLong',
       'city.coord.lat.$numberLong', 'rounded_lat', 'rounded_lon'],
      dtype='object')
```

## OpenWeatherMap Historical data

OpenWeatherMap provides an API returning the hourly Weather. A call to the API returns a maximum of 7 consecutive days of data.
[https://openweathermap.org/history](https://openweathermap.org/history) 

Here is an example of a call: `http://history.openweathermap.org/data/2.5/history/city?id={id}&type=hour&start={start}&end={end}&appid={YOUR_API_KEY}`

### the response from the history of OpenWeatherMap

The documentation of the **response from the history** of OpenWeatherMap is here: [https://openweathermap.org/weather-data](https://openweathermap.org/weather-data)

``` json
{
    "dt": 1587312000,
    "main": {
        "temp": 287.44,
        "feels_like": 284.3,
        "pressure": 1015,
        "humidity": 76,
        "temp_min": 287.04,
        "temp_max": 288.15
    },
    "wind": {
        "speed": 4.6,
        "deg": 40
    },
    "clouds": {
        "all": 77
    },
    "weather": [
        {
            "id": 500,
            "main": "Rain",
            "description": "light rain",
            "icon": "10d"
        }
    ],
    "rain": {
        "1h": 0.3
    }
},
```

# How to contribute to software development

* run `npm install` to install the standard-conventions package. A utility for versioning using semver [https://semver.org/](https://semver.org/) and CHANGELOG generation powered by Conventional Commits [https://conventionalcommits.org](https://conventionalcommits.org).

* commit your changes by using the scripts. read the specifications [https://www.conventionalcommits.org/en/v1.0.0/#specification](https://www.conventionalcommits.org/en/v1.0.0/#specification)
    * run `git commit -m "{build}{chore}{ci}{docs}{feat}{fix}{perf}{refactor}{revert}{style}{test}: xxx"`

* set the version of the code and amend the CHANGELOG with
    * `npm run patch` (from 0.0.0 to 0.0.1)
    * `npm run minor` (from 0.0.0 to 0.1.0)
    * `npm run major` (from 0.0.0 to 1.0.0)

* push the code including the tags
    * `npm run push`


# kaggle implementations

Kaggle has been used to build the ETL. Here are the utility scripts and notebooks that are available if you want to use get the weather data in Belgium

* bpost_be_postal_code
* altf1be_helpers


# Acronyms

* ETL: Extract-Transform-Load https://en.wikipedia.org/wiki/Extract,_transform,_load