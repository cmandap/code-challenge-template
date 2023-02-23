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


def update_weather_station_stats(update_conflicts=False):
    """
        Calculates weather station statistics for every year from the
        WeatherRecord model and update them into WeatherStationStats model.
        Ensures that only records to be created are created, records are updated
        otherwise.

        This implementation is made compatible with PostgreSQL. One might have to
        check the documentation for compatibility when trying to update the DB.

        Args:
            Accepts No Args.

        Returns:
            None.
    """
    start_time = datetime.now()

    try:
        # extract the statistical information directly from the WeatherRecord model
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

        records = [
            {
                "weather_station_id": record.get("weather_station"),
                **record,
            }
            for record in records
        ]
        [record.pop("weather_station") for record in records]

        if update_conflicts:
            # create all the records in bulk (for better performance).
            # The bulk_create with update_confilcts = True does a upsert operation.
            # Only total_yield and update_by are updated on unique constraint violation.
            created_records = WeatherStationStats.objects.bulk_create(
                [WeatherStationStats(**values) for values in records],
                update_conflicts=True,
                unique_fields=['weather_station', 'year'],
                update_fields=["avg_min_temp",
                               "avg_max_temp", "total_precipitation"],
                batch_size=1000)
        else:
            # Incase if update to the existing records is not desired
            created_records = WeatherStationStats.objects.bulk_create(
                [WeatherStationStats(**values) for values in records],
                ignore_conflicts=True,
                batch_size=1000)

        print(f"Inserted {len(created_records)} new weather station stats records\
            in {(datetime.now() - start_time).total_seconds()} seconds")
    except Exception as err:
        print(
            f"Encountered exception while calculating Stats")
        raise err


def run(*args):
    """
        This function is the starting point of script execution. Invoked
        automatically by the runscript.

        Args:
            Accepts no arguments.

        Returns:
            None.
    """
    update_weather_station_stats(True if 'update_conflicts' in args else False)
