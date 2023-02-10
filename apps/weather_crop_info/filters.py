from rest_framework.filters import BaseFilterBackend
import coreapi
import coreschema


class WeatherRecordFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
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
    def get_schema_fields(self, view):
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
