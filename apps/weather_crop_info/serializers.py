"""
    This module contains serializers for weather_crop_info app.

    Author: Chandrahas Reddy Mandapati 
"""
from rest_framework import serializers

from .models import WeatherRecord, WeatherStationStats


class WeatherRecordSerializer(serializers.ModelSerializer):
    """
        Model serializer responsible for WeatherRecord model.

        Dependencies:
            * WeatherRecordList
    """
    station_id = serializers.CharField(
        source="weather_station.station_id", read_only=True)

    class Meta:
        model = WeatherRecord
        exclude = ['weather_station']


class WeatherStationStatsSerializer(serializers.ModelSerializer):
    """
        Model serializer responsible for WeatherStationStats model.

        Dependencies:
            * WeatherStationStatsList
    """
    station_id = serializers.CharField(
        source="weather_station.station_id", read_only=True)

    class Meta:
        model = WeatherStationStats
        exclude = ['weather_station']
