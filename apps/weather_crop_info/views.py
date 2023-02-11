"""
    This module contains views for weather_crop_info app.

    Author: Chandrahas Reddy Mandapati 
"""
from datetime import datetime
from http import HTTPStatus

from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import (WeatherRecordFilterBackend,
                      WeatherStationStatsFilterBackend)
from .models import WeatherRecord, WeatherStationStats
from .serializers import WeatherRecordSerializer, WeatherStationStatsSerializer


class WeatherRecordList(APIView, PageNumberPagination):
    """
        This view must handle get and post requests for WeatherRecord model.
        Makes use of WeatherRecordSerializer.
        Makes use of PageNumberPagination.

        get:
        Return list of weather records and pagination information.
    """
    filter_backends = (WeatherRecordFilterBackend,)

    def get(self, request, format=None):
        queryset = WeatherRecord.objects.all()
        station_id = self.request.query_params.get('station-id')
        date = self.request.query_params.get('date')
        if station_id is not None:
            queryset = queryset.filter(
                weather_station__station_id__contains=station_id)
        if date is not None:
            try:
                date = datetime.strptime(date, '%Y%m%d')
                queryset = queryset.filter(date=date)
            except ValueError as e:
                return Response(status=HTTPStatus.BAD_REQUEST)
        weather_records_paginated = self.paginate_queryset(
            queryset, request, view=self)
        serializer = WeatherRecordSerializer(
            weather_records_paginated, many=True)
        return Response(serializer.data)


class WeatherStationStatsList(APIView, PageNumberPagination):
    """
        This view must handle get and post requests for WeatherStationStats model.
        Makes use of WeatherStationStatsSerializer.
        Makes use of PageNumberPagination.

        get:
        Return list of weather Station stats and pagination information.
    """
    filter_backends = (WeatherStationStatsFilterBackend,)

    def get(self, request, format=None):
        queryset = WeatherStationStats.objects.all()
        station_id = self.request.query_params.get('station-id')
        year = self.request.query_params.get('year')
        if station_id is not None:
            queryset = queryset.filter(
                weather_station__station_id__contains=station_id)
        if year is not None:
            queryset = queryset.filter(year=int(year))
        weather_station_stats_paginated = self.paginate_queryset(
            queryset, request, view=self)
        serializer = WeatherStationStatsSerializer(
            weather_station_stats_paginated, many=True)
        return Response(serializer.data)
