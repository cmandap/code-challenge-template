# Corteva Code Challenge
This repository is built in response to the corteva code challenge. The functionalities and design decisions are further discussed in detail under respective sections.
## Contents
1. [ Installation and Setup ](#inst)
2. [ Data Modeling](#dm)
3. [ Ingestion ](#ingestion)
4. [ Data Analysis ](#da)
5. [ Testing ](#testing)
6. [ REST API's ](#restapi)
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

