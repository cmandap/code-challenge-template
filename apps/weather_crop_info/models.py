"""
    This module maintains all the models required for weather_crop_info application.

    Author: Chandrahas Reddy Mandapati 
"""
from django.db import models


class WeatherStation(models.Model):
    """
        This model stores and maintains real world information about weather stations.
        Currently, station_id and station_name field holds the same data.
        Moreover, stores metadata for every row such as row creation and updation details.

        TODO: 
            * Move the row metadata information to a abstract model to avoid redundancy.
    """
    station_id = models.CharField(
        unique=True, max_length=200, verbose_name="Real World Station Reference")
    station_name = models.CharField(
        unique=True, max_length=200, verbose_name="Real World Station Name")
    create_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Application Record Created Date")
    create_by = models.CharField(
        max_length=200, verbose_name="Application Record Create Event")
    update_timestamp = models.DateTimeField(
        auto_now=True, verbose_name="Application Record Updated Date")
    update_by = models.CharField(
        max_length=200, verbose_name="Application Record Update Event")

    class Meta:
        db_table = 'weather_station'


class WeatherRecord(models.Model):
    """
        This models stores and maintains weather records captured at several weather stations.
        Maintains a foreign key to WeatherStation and enforces unique constraint on weather staion and date combination.
        Moreover, stores metadata for every row such as row creation and updation details.

        TODO: 
            * Move the row metadata information to a abstract model to avoid redundancy.
    """
    weather_station = models.ForeignKey(
        WeatherStation, on_delete=models.CASCADE, verbose_name="Application Generated Station Reference")
    date = models.DateTimeField(verbose_name="Weather Record Generated Date")
    min_temp = models.FloatField(null=True, verbose_name="Minimum Temperature")
    max_temp = models.FloatField(null=True, verbose_name="Maximum Temperature")
    precipitation = models.FloatField(
        null=True, verbose_name="Precipitation Level")
    create_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Application Record Created Date")
    create_by = models.CharField(
        max_length=200, verbose_name="Application Record Create Event")
    update_timestamp = models.DateTimeField(
        auto_now=True, verbose_name="Application Record Updated Date")
    update_by = models.CharField(
        max_length=200, verbose_name="Application Record Update Event")

    class Meta:
        db_table = 'weather_record'
        constraints = [
            models.UniqueConstraint(
                fields=['weather_station', 'date'], name='unique_station_date_constraint'
            )
        ]


class CropYieldRecord(models.Model):
    """
        This models stores and maintains crop yield information.
        Currently, only enforces year field to be unique but, can be extended to a couple of combinations.
        Moreover, stores metadata for every row such as row creation and updation details.

        TODO: 
            * Move the row metadata information to a abstract model to avoid redundancy.
    """
    year = models.PositiveIntegerField(unique=True,
                                       verbose_name="Record Generated Corresponding Year")
    total_yield = models.PositiveIntegerField(
        verbose_name="Total Yield per Year")
    create_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Application Record Created Date")
    create_by = models.CharField(
        max_length=200, verbose_name="Application Record Create Event")
    update_timestamp = models.DateTimeField(
        auto_now=True, verbose_name="Application Record Updated Date")
    update_by = models.CharField(
        max_length=200, verbose_name="Application Record Update Event")

    class Meta:
        db_table = 'crop_yield_record'


class WeatherStationStats(models.Model):
    """
        This model stores the statistical information of weather stations per year basis.
        Currently, enforces unique constraint on weather staion and date combination.
    """
    weather_station = models.ForeignKey(
        WeatherStation, on_delete=models.CASCADE, verbose_name="Application Generated Station Reference")
    year = models.PositiveIntegerField(
        verbose_name="Station Stats Corresponding Year")
    avg_max_temp = models.FloatField(
        null=True, verbose_name="Avergae Maximum Temperature per Year")
    avg_min_temp = models.FloatField(
        null=True, verbose_name="Average Minimum Temperature per Year")
    total_precipitation = models.FloatField(
        null=True, verbose_name="Total Precipitation per Year")

    class Meta:
        db_table = 'weather_station_stats'
        constraints = [
            models.UniqueConstraint(
                fields=['weather_station', 'year'], name='unique_station_year_constraint'
            )
        ]
