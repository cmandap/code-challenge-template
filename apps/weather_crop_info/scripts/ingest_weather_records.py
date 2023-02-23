"""
    This module is a django script used to update captured weather records from 
    a text file to WeatherStation and WeatherRecord models. 

    Dependencies:
        * Update "test_weather_station_stats" test in tests.py for
        every new functionality or updated functionality.
        * ingest_weather_records script will be affected on change.
"""
from apps.weather_crop_info.models import WeatherStation, WeatherRecord
from datetime import datetime
from os import listdir
from os.path import isfile, join
from django.conf import settings
from pathlib import Path
import multiprocessing as mp

# Need this for MacOS version since the default process start method has changed to 'spawn' from 'fork'
mp.set_start_method('fork', force=True)


def file_handler(file_path, update_conflicts=False):
    """
        A file handler that reads the weather information from the text file
        and updates the WeatherRecord model. Ensures that only records to be 
        created are created, records are updated otherwise. 

        This implementation is made compatible with PostgreSQL. One might have to
        check the documentation for compatibility when trying to update the DB.

        Args:
        file_path (String): file path related to BASE_DIR setting.

        Returns:
            int: Newly created records count.
            int: Updated records count.
    """
    start_time = datetime.now()

    try:
        # extract only the filename without extension.
        # this represents the weather station
        file_name = Path(file_path).stem

        # create the weather station record if one doesnt exists
        weather_station, created = WeatherStation.objects.get_or_create(
            station_id=file_name,
            station_name=file_name,
            create_by="ingest_weather_records_script",
            update_by="ingest_weather_records_script",
        )
        records = []

        # extract the records from the file
        with open(file_path, "r") as file:
            for record in file:
                date, max_temp, min_temp, precip = record.strip().split("\t")
                records.append(
                    {
                        "weather_station": weather_station,
                        "date": datetime.strptime(date, '%Y%m%d'),
                        "min_temp": None if int(min_temp) == -9999 else float(min_temp),
                        "max_temp": None if int(max_temp) == -9999 else float(max_temp),
                        "precipitation": None if int(precip) == -9999 else float(precip),
                        "create_by": "ingest_weather_records_script",
                        "update_by": "ingest_weather_records_script",
                    }
                )

        if update_conflicts:
            # create all the records in bulk (for better performance).
            # The bulk_create with update_confilcts = True does a upsert operation.
            # Only total_yield and update_by are updated on unique constraint violation.
            created_records = WeatherRecord.objects.bulk_create(
                [WeatherRecord(**values) for values in records],
                update_conflicts=True,
                unique_fields=['weather_station', 'date'],
                update_fields=["min_temp", "max_temp",
                               "precipitation", "update_by"],
                batch_size=1000)
        else:
            # Incase if update to the existing records is not desired
            created_records = WeatherRecord.objects.bulk_create(
                [WeatherRecord(**values) for values in records],
                ignore_conflicts=True,
                batch_size=1000)

        print(f"Inserted/Updated {len(created_records)} new records for the file {file_path}\
            in {(datetime.now() - start_time).total_seconds()} seconds")
        return len(created_records)
    except Exception as err:
        print(
            f"Encountered exception while operating on file {file_path}")
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
    start_time = datetime.now()
    inserted_records_count = 0

    # extract all the files in the folder set in settings.
    files = [join(settings.WEATHER_DATA_DIR, f) for f in listdir(
        settings.WEATHER_DATA_DIR) if isfile(join(settings.WEATHER_DATA_DIR, f))]

    # building function arguments to be assigned to process in pool
    pool_args = [[file, True if 'update_conflicts' in args else False]
                 for file in files]

    # process all the files parallely for faster execution.
    # TODO: configure pool size dynamically.
    with mp.Pool(5) as pool:
        inserted_records_counts = pool.starmap(file_handler, pool_args)

    # TODO : invoke calculate_weather_station_stats script automatically.
    print(
        f"Finally inserted {sum(inserted_records_counts)} new records in \
            {(datetime.now() - start_time).total_seconds()} seconds")
