from django.db import models


class WeatherStation(models.Model):
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
    weather_station_id = models.ForeignKey(
        WeatherStation, on_delete=models.CASCADE, db_column='weather_station_id', verbose_name="Application Generated Station Reference")
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
                fields=['weather_station_id', 'date'], name='unique_station_date_constraint'
            )
        ]


class CropYieldRecord(models.Model):
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
    weather_station_id = models.ForeignKey(
        WeatherStation, on_delete=models.CASCADE, db_column='weather_station_id', verbose_name="Application Generated Station Reference")
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
                fields=['weather_station_id', 'year'], name='unique_station_year_constraint'
            )
        ]
