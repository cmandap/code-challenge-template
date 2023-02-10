from apps.weather_crop_info.models import WeatherStation, WeatherRecord
from datetime import datetime
from os import listdir
from os.path import isfile, join
from django.conf import settings

import ntpath


def file_handler(file_path):
    start_time = datetime.now()

    file_name = ntpath.basename(file_path)
    weather_station, created = WeatherStation.objects.get_or_create(
        station_id=file_name,
        station_name=file_name,
        create_by="ingest_weather_records_script",
        update_by="ingest_weather_records_script",
    )
    records = []
    records_to_update = []
    records_to_create = []
    with open(file_path, "r") as file:
        for record in file:
            date, max_temp, min_temp, precip = record.strip().split("\t")
            records.append(
                {
                    "weather_station_id": weather_station,
                    "date": datetime.strptime(date, '%Y%m%d'),
                    "min_temp": None if int(min_temp) == -9999 else float(min_temp),
                    "max_temp": None if int(max_temp) == -9999 else float(max_temp),
                    "precipitation": None if int(precip) == -9999 else float(precip),
                    "create_by": "ingest_weather_records_script",
                    "update_by": "ingest_weather_records_script",
                }
            )

    records = [
        {
            "id": WeatherRecord.objects.filter(
                weather_station_id=weather_station.id,
                date=record.get("date")
            ).first().id
            if WeatherRecord.objects.filter(
                weather_station_id=weather_station.id,
                date=record.get("date")
            ).first() is not None
            else None,
            **record,
        }
        for record in records
    ]

    [records_to_update.append(record) if record["id"] is not None else records_to_create.append(
        record) for record in records]

    [record.pop("id") for record in records_to_create]

    [record.pop("create_by") for record in records_to_update]

    created_records = WeatherRecord.objects.bulk_create(
        [WeatherRecord(**values) for values in records_to_create], batch_size=1000)

    WeatherRecord.objects.bulk_update(
        [
            WeatherRecord(id=values.get("id"), min_temp=values.get("min_temp"), max_temp=values.get(
                "max_temp"), precipitation=values.get("precipitation"), update_by=values.get("update_by"))
            for values in records_to_update
        ],
        ["min_temp", "max_temp", "precipitation", "update_by"],
        batch_size=1000
    )

    print(f"Inserted {len(created_records)} new records for the file {file_path} in {(datetime.now() - start_time).total_seconds()} seconds")
    print(f"Updated {len(records_to_update)} new records for the file {file_path} in {(datetime.now() - start_time).total_seconds()} seconds")
    return len(created_records)


def run():
    start_time = datetime.now()
    inserted_records_count = 0
    files = [join(settings.WEATHER_DATA_DIR, f) for f in listdir(settings.WEATHER_DATA_DIR) if isfile(
        join(settings.WEATHER_DATA_DIR, f))]
    for file in files:
        inserted_records_count += file_handler(file)
    print(
        f"Finally inserted {inserted_records_count} new records in {(datetime.now() - start_time).total_seconds()} seconds")
