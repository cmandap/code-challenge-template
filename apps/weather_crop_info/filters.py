"""
    This module contains filters for weather_crop_info app.

    Author: Chandrahas Reddy Mandapati 
"""
import coreapi
import coreschema
from rest_framework.filters import BaseFilterBackend


class WeatherRecordFilterBackend(BaseFilterBackend):
    """
        Filter Backend handling filters for WeatherRecord model.
    """

    def get_schema_fields(self, view):
        """
            function responsible for providing schema fields to swagger doc
            for WeatherRecordList api.

            Returns:
                Api schema
        """
        return [coreapi.Field(
            name='station-id',
            location='query',
            required=False,
            description="Weather Station ID",
            schema=coreschema.String()
        ), coreapi.Field(
            name='date',
            location='query',
            description="Date in YYYYMMDD format",
            schema=coreschema.String(format="YYYYMMDD"),
            required=False
        ), coreapi.Field(
            name='page',
            location='query',
            description="Page Number",
            schema=coreschema.Integer(),
            required=False
        )]


class WeatherStationStatsFilterBackend(BaseFilterBackend):
    """
        Filter Backend handling filters for WeatherStationStats model.
    """

    def get_schema_fields(self, view):
        """
            function responsible for providing schema fields to swagger doc
            for WeatherStationStatsList api.

            Returns:
                Api schema
        """
        return [coreapi.Field(
            name='station-id',
            location='query',
            required=False,
            description="Weather Station ID",
            schema=coreschema.String()
        ), coreapi.Field(
            name='year',
            location='query',
            description="Year in YYYY format",
            schema=coreschema.String(format="YYYY"),
            required=False
        ), coreapi.Field(
            name='page',
            location='query',
            description="Page Number",
            schema=coreschema.Integer(),
            required=False
        )]
