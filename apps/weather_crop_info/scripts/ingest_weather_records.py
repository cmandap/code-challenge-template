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


def file_handler(file_path):
    """
        A file handler that reads the weather information from the text file
        and updates the WeatherRecord model. Ensures that only records to be 
        created are created, records are updated otherwise. 

        Args:
        file_path (String): file path related to BASE_DIR setting.

        Returns:
            int: Newly created records count.
            int: Updated records count.
    """
    start_time = datetime.now()

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
    records_to_update = []
    records_to_create = []

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

    # check what all records exists already based on the assumption that all the
    # existing records will have id.
    # TODO : populate records_to_update only if the corresponsing fields have changed
    records = [
        {
            "id": WeatherRecord.objects.filter(
                weather_station=weather_station.id,
                date=record.get("date")
            ).first().id
            if WeatherRecord.objects.filter(
                weather_station=weather_station.id,
                date=record.get("date")
            ).first() is not None
            else None,
            **record,
        }
        for record in records
    ]

    [records_to_update.append(record) if record["id"] is not None else
        records_to_create.append(record) for record in records]

    [record.pop("id") for record in records_to_create]

    [record.pop("create_by") for record in records_to_update]

    # create all the records in bulk (for better performance).
    created_records = WeatherRecord.objects.bulk_create(
        [WeatherRecord(**values) for values in records_to_create],
        batch_size=1000)

    # update all the records in bulk
    WeatherRecord.objects.bulk_update(
        [
            WeatherRecord(id=values.get("id"), min_temp=values.get("min_temp"),
                          max_temp=values.get("max_temp"), precipitation=values.get(
                "precipitation"), update_by=values.get("update_by"))
            for values in records_to_update
        ],
        ["min_temp", "max_temp", "precipitation", "update_by"],
        batch_size=1000
    )

    print(f"Inserted {len(created_records)} new records for the file {file_path}\
         in {(datetime.now() - start_time).total_seconds()} seconds")
    print(f"Updated {len(records_to_update)} new records for the file {file_path}\
         in {(datetime.now() - start_time).total_seconds()} seconds")
    return len(created_records), len(records_to_update)


def run():
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
    updated_records_count = 0

    # extract all the files in the folder set in settings.
    files = [join(settings.WEATHER_DATA_DIR, f) for f in listdir(
        settings.WEATHER_DATA_DIR) if isfile(join(settings.WEATHER_DATA_DIR, f))]

    # TODO : process all the files parallely for faster execution.
    for file in files:
        ret += file_handler(file)
        inserted_records_count += ret[0]
        updated_records_count += ret[1]
    print(
        f"Finally inserted {inserted_records_count} new records in \
            {(datetime.now() - start_time).total_seconds()} seconds")
