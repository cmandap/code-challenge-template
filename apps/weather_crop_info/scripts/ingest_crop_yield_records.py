"""
    This module is a django script used to update captured crop yeild records 
    from a text file to CropYieldRecord models. 

    Dependencies:
        * Update "test_crop_yield_records_data_ingestion" test in tests.py for
        every new functionality or updated functionality.
"""
from apps.weather_crop_info.models import CropYieldRecord
from datetime import datetime
from os import listdir
from os.path import isfile, join
from django.conf import settings
from itertools import repeat
import multiprocessing as mp

# Need this for MacOS version since the default process start method has changed to 'spawn' from 'fork'
mp.set_start_method('fork', force=True)


def file_handler(file_path, update_conflicts=False):
    """
        A file handler that reads the crop yield information from the text file
        and updates the CropYieldRecord model. Ensures that only records to be 
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

    records = []

    try:
        # extract the records from the file
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

        if update_conflicts:
            # create all the records in bulk (for better performance).
            # The bulk_create with update_confilcts = True does a upsert operation.
            # Only total_yield and update_by are updated on unique constraint violation.
            created_records = CropYieldRecord.objects.bulk_create(
                [CropYieldRecord(**values) for values in records],
                update_conflicts=True,
                unique_fields=['year'],
                update_fields=['total_yield', 'update_by'],
                batch_size=1000)
        else:
            # Incase if update to the existing records is not desired
            created_records = CropYieldRecord.objects.bulk_create(
                [CropYieldRecord(**values) for values in records],
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

    # extract all the files in the folder set in settings.
    files = [join(settings.CROP_YIELD_DATA_DIR, f)
             for f in listdir(settings.CROP_YIELD_DATA_DIR) if isfile(
        join(settings.CROP_YIELD_DATA_DIR, f))]

    # building function arguments to be assigned to process in pool
    pool_args = [[file, True if 'update_conflicts' in args else False]
                 for file in files]

    # process all the files parallely for faster execution.
    with mp.Pool(5) as pool:
        inserted_records_counts = pool.starmap(file_handler, pool_args)
    print(
        f"Finally updated {sum(inserted_records_counts)} new records in \
        {(datetime.now() - start_time).total_seconds()} seconds")
