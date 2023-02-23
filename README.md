# Corteva Code Challenge
This repository is built in response to the corteva code challenge. The functionalities and design decisions are further discussed in detail under respective sections.
## Contents
1. [ Installation and Setup ](#inst)
2. [ Data Modeling](#dm)
3. [ Ingestion ](#ingestion)
4. [ Data Analysis ](#da)
5. [ REST API's ](#restapi)
6. [ Testing ](#testing)
7. [ Swagger Docs](#swagger)
8. [ Deployment ](#deploy)

<a name="inst"></a>
<h2>Installation & Setup</h2>
Follow the below guidelines to get the application running. All the commands provided below are in compliance with the macOS. Look for corresponsding command online when working on different operating systems. 
<h3> Requirements </h3>

<br/>After cloing the github repository, create a virtual environment by executing the following command.

```
python3 -m venv <env_name>
```

<br/>Activate the virtual environment by execcuting the following command.
```
source <env_name>/bin/activate
```
<br/>Now, install the dependencies by executing the following command.
```
pip install -r requirements.txt
```
<br/>

<h3>Database Setup</h3>

<br/>Install the posgresql database depending on your operating system. Execute the following commands to create database, user and grant required roles to the created user.

```
brew install postgresql
sudo -u postgres psql
CREATE DATABASE cortevadb;
CREATE USER admin WITH PASSWORD 'admin';
GRANT ALL PRIVILEGES ON DATABASE cortevadb TO admin;
ALTER ROLE admin SET client_encoding TO 'utf8';
ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE admin SET timezone TO 'UTC';
```

<br/>Execute the following command to migrate all the migrations to the database
```
python manage.py migrate
```

<h3>Runserver</h3>

<br/>Bring the server by executing the following command.
```
python manage.py runserver
```

<a name="dm"></a>
<h2>Data Modeling</h2>

The ORM's data definition and model semantics for the data models can be found in [models.py](https://github.com/cmandap/code-challenge-template/blob/6ed8823b97a3a5d80dbd23f54a4a764d777d4f9a/apps/weather_crop_info/models.py).
There is a dedicated table maintained for weather station to obtain extensibility factor to store a couple of station information if needed in future.
Models WeatherRecord and WeatherStationStats maintain a foreign key reference to the WeatherStation.
Models WeatherRecord, WeatherStation, and CropYieldRecord models maintain row metadata for additional information.

<a name="ingestion"></a>
<h2>Data Ingestion</h2>
Data ingestion scripts to populate the weather, crop yield data from files to models can be found under [scripts](https://github.com/cmandap/code-challenge-template/tree/main/apps/weather_crop_info/scripts) folder. Both scripts [ingest_crop_yield_records](https://github.com/cmandap/code-challenge-template/blob/main/apps/weather_crop_info/scripts/ingest_crop_yield_records.py) and [ingest_weather_records](https://github.com/cmandap/code-challenge-template/blob/main/apps/weather_crop_info/scripts/ingest_weather_records.py) ensures that only missing records are created, records are updated otherwise. Currently, the files are being processed sequentially in both the scripts. Parallel processing of files will result in better performance therefore, a TODO for the same has been created.

<br/>The scripts can be executed by running the following command.
```
python manage.py runscript <file_name_without_.py_extension>
```
<br/> To update the conflict records due to unique constraint violation, execute the following commang.
```
python manage.py runscript <file_name_without_.py_extension> --script-args update_conflicts
```

<a name="da"></a>
<h2>Data Analysis</h2>
The script [calculate_weather_station_stats]() is used to calculate weather station statistics. All the missing data is ignored while calculating the statistics.

<a name="restapi"></a>
<h2>REST API's</h2>

<br/>The following endpoints are made available to operate on data.
```
/api/weather
/api/weather/stats
```

Both the endpoints establish a filter on top of station ID and date fields. Moreover, additional field called page is used to work around with the pagination. The page size is fixed to 10 and the same can be updated through [settings.py](https://github.com/cmandap/code-challenge-template/blob/main/django_project/settings.py).

Note that the endpoints are prefixed with ``` weather-crop-info/v1 ``` to represent the app to which the endpoints belong to and the current version of the app.

<a name="testing"></a>
<h2>Running Tests</h2>

<br/>Tests for scripts and views serving the endpoints are written under [tests.py](https://github.com/cmandap/code-challenge-template/blob/main/apps/weather_crop_info/tests.py) file. To execute the tests run the following command.
```
python manage.py test
```

<a name="swagger"></a>
<h2>Swagger Doc</h2>

<br/> A swagger document has been created for all the defined endpoints and can be accessed by the following endpoint.
```
/doc
```

<a name="deploy"></a>
<h2>Deployment</h2>

I would do the following to deploy the code on to AWS cloud.
* Create two ec2 intances, one for serving the application and one serving the database and make sure they are created under a VPN.
* Establish a CI/CD pipeline for the continuous deployment either by using jenkins or github worflow
* Set the cron job on top of data ingetion scripts.
* Set up Cloudwatch alarms to monitor the application logs.
* Set up nginix to serve as a reverse proxy for the server.
* Enable Auto Scaling on instances to auto deploy additional instances to handle more client connections.



