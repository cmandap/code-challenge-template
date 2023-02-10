from apps.weather_crop_info.models import CropYieldRecord
from datetime import datetime
from os import listdir
from os.path import isfile, join
from django.conf import settings


def file_handler(file_path):
    start_time = datetime.now()

    records = []
    records_to_update = []
    records_to_create = []
    with open(file_path, "r") as file:
        for record in file:
            year, total_yield = map(int, record.strip().split("\t"))
            records.append(
                {
                    "year": year,
                    "total_yield": total_yield,
                    "create_by": "ingest_crop_yield_records_script",
                    "update_by": "ingest_crop_yield_records_script",
                }
            )

    records = [
        {
            "id": CropYieldRecord.objects.filter(
                year=record.get("year")
            ).first().id
            if CropYieldRecord.objects.filter(
                year=record.get("year")
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

    created_records = CropYieldRecord.objects.bulk_create(
        [CropYieldRecord(**values) for values in records_to_create], batch_size=1000)

    CropYieldRecord.objects.bulk_update(
        [
            CropYieldRecord(id=values.get("id"), total_yield=values.get(
                "total_yield"), update_by=values.get("update_by"))
            for values in records_to_update
        ],
        ["total_yield"],
        batch_size=1000
    )

    print(f"Inserted {len(created_records)} new records for the file {file_path} in {(datetime.now() - start_time).total_seconds()} seconds")
    print(f"Updated {len(records_to_update)} new records for the file {file_path} in {(datetime.now() - start_time).total_seconds()} seconds")
    return len(created_records)


def run():
    start_time = datetime.now()
    inserted_records_count = 0
    files = [join(settings.CROP_YIELD_DATA_DIR, f) for f in listdir(settings.CROP_YIELD_DATA_DIR) if isfile(
        join(settings.CROP_YIELD_DATA_DIR, f))]
    for file in files:
        inserted_records_count += file_handler(file)
    print(
        f"Finally inserted {inserted_records_count} new records in {(datetime.now() - start_time).total_seconds()} seconds")
