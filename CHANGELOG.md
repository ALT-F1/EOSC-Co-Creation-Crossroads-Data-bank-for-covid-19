# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

### [2.0.8](https://github.com/ALT-F1/OpenWeatherMap/compare/v2.0.7...v2.0.8) (2020-06-11)


### Chores

* set the LICENSE to EUROPEAN UNION PUBLIC LICENCE v. 1.2 ([17fa084](https://github.com/ALT-F1/OpenWeatherMap/commit/17fa084fe6f32599eb8e0581ab4c71fcf854b31b))


### Documentations

* add sub-headings to improve the visibility of the sponsors, add info about ALT-F1 ([2fdefe2](https://github.com/ALT-F1/OpenWeatherMap/commit/2fdefe22566ac49cb88cf386dc095c9513aa6100))

### [2.0.7](https://github.com/ALT-F1/OpenWeatherMap/compare/v2.0.6...v2.0.7) (2020-06-11)


### Bug Fixes

* [#1](https://github.com/ALT-F1/OpenWeatherMap/issues/1) update the generation of 3 dates: June 08-09-10, 2020 ([ea3d5cf](https://github.com/ALT-F1/OpenWeatherMap/commit/ea3d5cf5a20b53e6c5f4749a55cc35f319d67a45))

### [2.0.6](https://github.com/ALT-F1/OpenWeatherMap/compare/v2.0.5...v2.0.6) (2020-06-11)


### Features

* add new weather data from June 01, 2020 ([5e7a16c](https://github.com/ALT-F1/OpenWeatherMap/commit/5e7a16c2c5fb5c31a62a130f6b0352739d213546))


### Documentations

* add June 08-09-10, 2020 ([b8f014e](https://github.com/ALT-F1/OpenWeatherMap/commit/b8f014e8bdf530ba2aad2647e71b45d040750f47))

### [2.0.5](https://github.com/ALT-F1/OpenWeatherMap/compare/v2.0.4...v2.0.5) (2020-06-08)


### Styles

* update the picture containing the logo of the contributors to the project ([0fc761d](https://github.com/ALT-F1/OpenWeatherMap/commit/0fc761db0d00ddc0d752d2e7a727d327bcc882f7))

### [2.0.4](https://github.com/ALT-F1/OpenWeatherMap/compare/v2.0.3...v2.0.4) (2020-06-08)


### Documentations

* correct grammar and misspellings ([cdcdc1e](https://github.com/ALT-F1/OpenWeatherMap/commit/cdcdc1ef95dbfb0870e72cc2274fb2b33194c64d))

### [2.0.3](https://github.com/ALT-F1/OpenWeatherMap/compare/v2.0.2...v2.0.3) (2020-06-08)


### Documentations

* add the section '# What are the data available?', rename a heading and the title ([913507e](https://github.com/ALT-F1/OpenWeatherMap/commit/913507e91cf64c6ede61187b1c1b7c877e700f99))

### [2.0.2](https://github.com/ALT-F1/OpenWeatherMap/compare/v2.0.1...v2.0.2) (2020-06-08)


### Documentations

* remove some text ([98507e2](https://github.com/ALT-F1/OpenWeatherMap/commit/98507e2d8fc1de193b32740367c55995048284b8))

### [2.0.1](https://github.com/ALT-F1/OpenWeatherMap/compare/v2.0.0...v2.0.1) (2020-06-08)


### Chores

* add first time the weather data compiled in one file, from 2020-03-01 to 2020-06-07 under output_directory/data/latest/by_province_and_quartile.csv ([c730dc5](https://github.com/ALT-F1/OpenWeatherMap/commit/c730dc5024662f368042478387be47cd68a3fcd6))

## [2.0.0](https://github.com/ALT-F1/OpenWeatherMap/compare/v1.4.2...v2.0.0) (2020-06-08)


### Features

* create one CSV file containing all dates for the weather stored in output_directory/data/by_province_and_quartile ([78836da](https://github.com/ALT-F1/OpenWeatherMap/commit/78836dadc328a53252f60fb845b75460afc72ca1))

### [1.4.2](https://github.com/ALT-F1/OpenWeatherMap/compare/v1.4.1...v1.4.2) (2020-06-08)


### Chores

* remove files that were under export_from_openweathermap directory due to a change in the tree structure ([b46ac62](https://github.com/ALT-F1/OpenWeatherMap/commit/b46ac62a6f3c3a8204b6026d06ad0bde420e60f2))
* remove the first version of the generation of the weather data ([7a79526](https://github.com/ALT-F1/OpenWeatherMap/commit/7a79526ab2860da37c86b54f0b248eb15d2dac63))

### [1.4.1](https://github.com/ALT-F1/OpenWeatherMap/compare/v1.4.0...v1.4.1) (2020-06-08)


### Chores

* add weather data per day collected from OpenWeatherMap.org and add aggregated weather data by province including the quantiles 25-50-75 ([1807ae8](https://github.com/ALT-F1/OpenWeatherMap/commit/1807ae86b311de3c8207d6d74a0cb2f71747d62b))
* delete useless historical data since all output data are stored in output_directory ([09d1099](https://github.com/ALT-F1/OpenWeatherMap/commit/09d1099ff1d098c88c781e32e536f3b1cbd8a904))

## [1.4.0](https://github.com/ALT-F1/OpenWeatherMap/compare/v1.3.2...v1.4.0) (2020-06-08)


### Features

* add a method: translate Belgian provinces in French ([33ffbc0](https://github.com/ALT-F1/OpenWeatherMap/commit/33ffbc062814d0632077577432180733dbea215f))
* create a directory by_date/yyy-mm-dd/*.{json|csv} containing OpenWeatherMap.org for Belgian cities, and group the weather data by province, and add quantiles 25-50-75 for main.temp, main.feels_like, main.pressure, main.humidity, main.temp, wind.speed, wind.deg ([4da4114](https://github.com/ALT-F1/OpenWeatherMap/commit/4da4114e7ccf53c3b26d35b548c1b4eebe955f46))


### Documentations

* add further method' documentation based on python3 best practice ([a8a3a95](https://github.com/ALT-F1/OpenWeatherMap/commit/a8a3a9502498b1ff7dc8d6df0dc49e833fb2f0f5))
* add further method' documentatoin ([0d8ff91](https://github.com/ALT-F1/OpenWeatherMap/commit/0d8ff917f833fa5c9085d366cb10161309cba6ed))

### [1.3.2](https://github.com/ALT-F1/OpenWeatherMap/compare/v1.3.1...v1.3.2) (2020-06-07)


### Refactorings

* rename the library to bpost_be_postal_code_helpers.py ([d9d2130](https://github.com/ALT-F1/OpenWeatherMap/commit/d9d2130a2d956ecf4cf3ea8786344d61c9aadb40))


### Styles

* remove the github social preview made with Pinta ([7172453](https://github.com/ALT-F1/OpenWeatherMap/commit/7172453e42cd1e0f26234454a351ad1353546f5f))

### [1.3.1](https://github.com/ALT-F1/OpenWeatherMap/compare/v1.3.0...v1.3.1) (2020-06-07)


### Chores

* delete input files moved under the same directory as it was stored on Kaggle ([84962a5](https://github.com/ALT-F1/OpenWeatherMap/commit/84962a5cae39104305f1f7b2a96ec58b2abe312e))
* delete unused files ([765cb0a](https://github.com/ALT-F1/OpenWeatherMap/commit/765cb0a30d5ca18b2adde66a04124d493e6cdfc2))


### Refactorings

* add get_history method to download the OpenWeatherMap.org, load history city list like it is stored on kaggle, add build_df method to separate the initialization of properties and build the DataFrame ([0bbdc73](https://github.com/ALT-F1/OpenWeatherMap/commit/0bbdc7321598004919efbf741d85d6ce97a9679c))
* create a class to ease the use of the methods, output_directory use the separator / or \ depending on the operating system ([06e0d42](https://github.com/ALT-F1/OpenWeatherMap/commit/06e0d42845c9c851b7d78db1f86601885a0766c4))
* move the file in the same directory as it was stored on Kaggle ([a8e15f5](https://github.com/ALT-F1/OpenWeatherMap/commit/a8e15f5b3a601b2c8ce30030ae83378fc98c3954))
* use AltF1BeHelpers class instead of functions ([aa68849](https://github.com/ALT-F1/OpenWeatherMap/commit/aa688496a9a6889095760236f27f461a5daa41e2))
* use AltF1BeHelpers class instead of functions, move openweathermap_get_history into openweathermap_helpers.py, add usage example of the class ([dd25155](https://github.com/ALT-F1/OpenWeatherMap/commit/dd25155ca118c5a58774022f57e9b5e564a199ed))

## [1.3.0](https://github.com/ALT-F1/OpenWeatherMap/compare/v1.2.1...v1.3.0) (2020-06-06)


### Features

* altf1be_helpers.py checks if you use an interactive app such as kaggle, convert unicode to ascii, set the output directory and set a date range ([966bfdc](https://github.com/ALT-F1/OpenWeatherMap/commit/966bfdcac11109de89dc50d0e5136bcb816bcd1c))
* BPost_postal_codes extract-transform-load postal codes metadata from bpost.be to manipulate them ([899af49](https://github.com/ALT-F1/OpenWeatherMap/commit/899af49903b8c4996d02b5cad28a62b185c2f644))
* merge OpenWeatherMap.org and BPost.be cities and postal codes and store them under output_directory/data/YYY-MM-DD directories ([1237115](https://github.com/ALT-F1/OpenWeatherMap/commit/123711578b54673a6f265f28b8e9cb28c346f1b4))
* OpenWeatherMap class extract-transform-load cities from OpenWeatherMap.org to manipulate them ([069e2ff](https://github.com/ALT-F1/OpenWeatherMap/commit/069e2ff07748f24705ce3fdf4b88583f228d60f5))


### Bug Fixes

* rename create_pd to csv_to_df to facilitate the understanding ([b3c5bea](https://github.com/ALT-F1/OpenWeatherMap/commit/b3c5bea15e918ffd87d43475409f2a12cd5763db))


### Documentations

* add 'how to run the code' section ([a11a44e](https://github.com/ALT-F1/OpenWeatherMap/commit/a11a44e51843cbe6b3b50109f213ec3d76f36adf))
* correct misspellings ([7509ea5](https://github.com/ALT-F1/OpenWeatherMap/commit/7509ea5d3386859ce95739e60623cdf0b0a1d2f3))


### Chores

* add .json and .csv in .gitattributes ([d6db11a](https://github.com/ALT-F1/OpenWeatherMap/commit/d6db11a9f4315cd9a72f87fef2d3bc8b4c6e8a69))
* store BPost.be postal codes ([e987090](https://github.com/ALT-F1/OpenWeatherMap/commit/e987090564011461cbfb2d4625f4ca8c732252f6))


### Styles

* add github social preview ([bbe9a1c](https://github.com/ALT-F1/OpenWeatherMap/commit/bbe9a1cd223d4e818ac5beaefc12be5476b20030))

### [1.2.1](https://github.com/ALT-F1/OpenWeatherMap/compare/v1.2.0...v1.2.1) (2020-05-24)


### Features

* store temporary files (dataframes) under a 'tmp' directory ([7504cf9](https://github.com/ALT-F1/OpenWeatherMap/commit/7504cf9edcc18dd1ba08964d5486dc4ef4338075))

## [1.2.0](https://github.com/ALT-F1/OpenWeatherMap/compare/v1.1.0...v1.2.0) (2020-05-24)


### Features

* generate the weather data in Belgium from March 01, 2020 to May 22, 2020 in csv format ([218133f](https://github.com/ALT-F1/OpenWeatherMap/commit/218133f7d42aee42973f452056556ca5e37ac59f))


### Chores

* add src/data/export_from_openweathermap/historical/csv-March_2020-to-May_22_2020 to gitignore ([85737be](https://github.com/ALT-F1/OpenWeatherMap/commit/85737be6b0b13d3ba75ec5b12dd7540ac6dc0da9))

## [1.1.0](https://github.com/ALT-F1/OpenWeatherMap/compare/v1.0.0...v1.1.0) (2020-05-22)


### Features

* export openweathermap.org historical data in json ([d7175a8](https://github.com/ALT-F1/OpenWeatherMap/commit/d7175a899b16ff50b02d99a192b35e9c6bb9e8da))

## 1.0.0 (2020-05-21)


### Features

* create a dataframe containing the cities and postal codes, then get the weather data for each city ([55e6678](https://github.com/ALT-F1/OpenWeatherMap/commit/55e6678ce5b08d0a402917601062239c3be4ce06))


### Documentations

* describe the project in details ([b470429](https://github.com/ALT-F1/OpenWeatherMap/commit/b470429f1c5c835f86339d9a52299794d694f8f5))
* set the license to alt-f1.be ALT-F1 SPRL ([c3c8a39](https://github.com/ALT-F1/OpenWeatherMap/commit/c3c8a3937178511250b1ab93fe0ef409e0cdb958))
* store the belgian postal codes in French and Dutch ([a600d05](https://github.com/ALT-F1/OpenWeatherMap/commit/a600d05cabc537bd61b46891cf84744532989d5a))
* store the cities list recognized by openweathermap.org ([31ff5d1](https://github.com/ALT-F1/OpenWeatherMap/commit/31ff5d1a41190995d372adf77a006f824ae8a338))
* store the weather data from cities in Belgium collected from openweathermap.org ([4584a24](https://github.com/ALT-F1/OpenWeatherMap/commit/4584a24b9053ddbb68092520e86431d6483eded0))
* store the weather data from cities in Belgium collected from openweathermap.org ([cfcd6ad](https://github.com/ALT-F1/OpenWeatherMap/commit/cfcd6add9be2db9146c8e582ba67f1d9d8d9e433))
* store the weather data from cities in Belgium collected from openweathermap.org ([046f314](https://github.com/ALT-F1/OpenWeatherMap/commit/046f3149cd28d32832d24d20018501b3518d1558))


### Builds

* define the configuration of the project ([d72cc45](https://github.com/ALT-F1/OpenWeatherMap/commit/d72cc4580d080b43fb22fe20e86e640074d6b5f2))
* set the libraries required to run the code ([4f05630](https://github.com/ALT-F1/OpenWeatherMap/commit/4f0563021fadb42ce3fe5350e3f31289651fce17))
* set the local environment with conda named 'pandas' ([f1d4e31](https://github.com/ALT-F1/OpenWeatherMap/commit/f1d4e31ad0396513a3e9e941c1f0f281098da730))


### Chores

* add .gitignore matching those file types: node,python,jupyternotebooks,visualstudiocode ([48055b1](https://github.com/ALT-F1/OpenWeatherMap/commit/48055b1fb2a99e0a0affad85c8b3a9d2a8f40abe))
* add custom .gitattributes ([0a884f2](https://github.com/ALT-F1/OpenWeatherMap/commit/0a884f2ed26d279446988e8a3848edc06c564b58))
* set the .gitignore for node, python, jupyternotebooks, visualstudiocode ([9a3dba1](https://github.com/ALT-F1/OpenWeatherMap/commit/9a3dba19f50650e07094890999df756e3b0bac79))
* set the debug configuration ([c4c92a3](https://github.com/ALT-F1/OpenWeatherMap/commit/c4c92a3244f5fa9bad146abca22a1e08f9d27d8a))
* set the visible headers in the CHANGELOG ([fb07a72](https://github.com/ALT-F1/OpenWeatherMap/commit/fb07a7213a2f478b8398e0be358857461f194762))
