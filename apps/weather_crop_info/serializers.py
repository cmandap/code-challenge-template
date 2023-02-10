from rest_framework import serializers
from .models import WeatherRecord, WeatherStationStats


class WeatherRecordSerializer(serializers.ModelSerializer):
    station_id = serializers.CharField(
        source="weather_station.station_id", read_only=True)

    class Meta:
        model = WeatherRecord
        exclude = ['weather_station']


class WeatherStationStatsSerializer(serializers.ModelSerializer):
    station_id = serializers.CharField(
        source="weather_station.station_id", read_only=True)

    class Meta:
        model = WeatherStationStats
        exclude = ['weather_station']
