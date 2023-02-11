"""
    This module is a django script used to update captured weather statistics
    from WeatherRecord model to WeatherStationStats model.

    Dependencies:
        * Update "test_weather_station_stats" test in tests.py for
        every new functionality or updated functionality.
        * ingest_weather_records script will be affected on change.
"""
from apps.weather_crop_info.models import WeatherStationStats, WeatherRecord
from django.db.models import Avg, Sum
from django.db.models import F
from datetime import datetime


def update_weather_station_stats():
    """
        Calculates weather station statistics for every year from the
        WeatherRecord model and update them into WeatherStationStats model.
        Ensures that only records to be created are created, records are updated
         otherwise.

        Args:
            Accepts No Args.

        Returns:
            None.
    """
    start_time = datetime.now()
    records = WeatherRecord.objects.values(
        'weather_station',
        year=F('date__year')
    ).annotate(
        avg_max_temp=Avg('max_temp'),
        avg_min_temp=Avg('min_temp'),
        total_precipitation=Sum('precipitation'),
    ).exclude(
        max_temp__isnull=True,
        min_temp__isnull=True,
        precipitation__isnull=True
    )
    records_to_update = []
    records_to_create = []

    records = [
        {
            "id": WeatherStationStats.objects.filter(
                weather_station=record.get("weather_station"),
                year=record.get("year")
            ).first().id
            if WeatherStationStats.objects.filter(
                weather_station=record.get("weather_station"),
                year=record.get("year")
            ).first() is not None
            else None,
            **record,
        }
        for record in records
    ]

    [records_to_update.append(record) if record["id"] is not None
        else records_to_create.append(record) for record in records]

    [record.pop("id") for record in records_to_create]
    records_to_create = [
        {
            "weather_station_id": record.get("weather_station"),
            **record,
        }
        for record in records_to_create
    ]
    [record.pop("weather_station") for record in records_to_create]

    created_records = WeatherStationStats.objects.bulk_create(
        [WeatherStationStats(**values) for values in records_to_create],
        batch_size=1000)

    WeatherStationStats.objects.bulk_update(
        [
            WeatherStationStats(id=values.get("id"), avg_max_temp=values.get(
                "avg_max_temp"), avg_min_temp=values.get(
                "avg_min_temp"), total_precipitation=values.get(
                "total_precipitation"))
            for values in records_to_update
        ],
        ["avg_min_temp", "avg_max_temp", "total_precipitation"],
        batch_size=1000
    )

    print(f"Inserted {len(created_records)} new weather station stats records\
         in {(datetime.now() - start_time).total_seconds()} seconds")
    print(f"Updated {len(records_to_update)} new weather station stats records\
         in {(datetime.now() - start_time).total_seconds()} seconds")


def run():
    """
        This function is the starting point of script execution. Invoked
        automatically by the runscript.

        Args:
            Accepts no arguments.

        Returns:
            None.
    """
    update_weather_station_stats()
