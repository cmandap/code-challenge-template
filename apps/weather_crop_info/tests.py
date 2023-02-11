"""
    This module contains tests for weather_crop_info app. Test classes are 
    seperated based on model, views and controllers.
"""
import os
from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from .models import (CropYieldRecord, WeatherRecord, WeatherStation,
                     WeatherStationStats)
from .scripts.calculate_weather_station_stats import \
    update_weather_station_stats
from .scripts.ingest_crop_yield_records import \
    file_handler as crop_yield_file_handler
from .scripts.ingest_weather_records import \
    file_handler as weather_record_file_handler


class DataIngestionTestCase(TestCase):
    """
        This class is responsible for defining tests for weather_crop_info scripts.


    """

    def setUp(self):
        """
            This method handles all the testcase setup. Executed before
            every test case is invoked. Invoked once per every testcase not per 
            class.

            Args:
                self.

            Returns:
                None
        """
        self.station_id = "USC00000072"
        self.weather_record_file_name = "/tmp/USC00000072.txt"
        self.crop_yield_file_name = "/tmp/crop_yield_data.txt"
        test_weather_records = [
            [19850101, -22, -128, 94], [19850102, -122, -217, 0]]
        test_crop_yield_records = [[1985, 225447], [1986, 208944]]
        with open(self.weather_record_file_name, "w+") as file:
            file.writelines(['\t'.join(map(str, record)) + '\n'
                             for record in test_weather_records])
        with open(self.crop_yield_file_name, "w+") as file:
            file.writelines(['\t'.join(map(str, record)) + '\n'
                             for record in test_crop_yield_records])

    def test_weather_records_data_ingestion(self):
        """
            This method tests the data ingestion script for updating weather
            records in the model.

            Args:
                self.

            Returns:
                None
        """
        weather_record_file_handler(self.weather_record_file_name)
        weather_station = WeatherStation.objects.get(
            station_id=self.station_id)
        self.assertEqual(weather_station.station_id, self.station_id)
        query_date = datetime.strptime("19850101", "%Y%m%d")
        weather_record = WeatherRecord.objects.get(
            weather_station_id=weather_station.id, date=query_date)
        self.assertEqual(weather_record.min_temp, float(-128))
        weather_records = WeatherRecord.objects.all()
        self.assertEqual(len(weather_records), 2)

    def test_crop_yield_records_data_ingestion(self):
        """
            This method tests the data ingestion script for updating crop
            yeild records in the model.

            Args:
                self.

            Returns:
                None
        """
        crop_yield_file_handler(self.crop_yield_file_name)
        crop_yield_records = CropYieldRecord.objects.all()
        self.assertEqual(len(crop_yield_records), 2)
        crop_yield_record = CropYieldRecord.objects.get(year=1985)
        self.assertEqual(crop_yield_record.total_yield, 225447)

    def test_weather_station_stats(self):
        """
            This method tests the data analysis script for calculating the 
            weather station statistics and updating them into model.

            Args:
                self.

            Returns:
                None
        """
        weather_record_file_handler(self.weather_record_file_name)
        update_weather_station_stats()
        weather_station = WeatherStation.objects.get(
            station_id=self.station_id)
        station_stats = WeatherStationStats.objects.all()
        self.assertEqual(len(station_stats), 1)
        station_stats_record = WeatherStationStats.objects.get(
            weather_station_id=weather_station.id, year=1985)
        self.assertEqual(station_stats_record.avg_max_temp, float(-72))

    def tearDown(self):
        """
            This method is responsible for removing the setup that was created
            before execution of testcase. Invoked after every testcase.

            Args:
                self.

            Returns:
                None
        """
        os.remove("/tmp/USC00000072.txt")


class WeatherAPITestCase(TestCase):
    def setUp(self):
        """
            This method handles all the testcase setup. Executed before
            every test case is invoked. Invoked once per every testcase not per 
            class.

            Args:
                self.

            Returns:
                None
        """
        self.station_id = "USC00000072"
        self.weather_record_file_name = "/tmp/USC00000072.txt"
        test_weather_records = [
            [19850101, -22, -128, 94], [19850102, -122, -217, 0]]
        with open(self.weather_record_file_name, "w+") as file:
            file.writelines(['\t'.join(map(str, record)) + '\n'
                             for record in test_weather_records])

    def test_weather_api(self):
        """
            This method tests the WeatherRecordList view.

            Args:
                self.

            Returns:
                None
        """
        weather_record_file_handler(self.weather_record_file_name)
        self.assertEqual('/weather-crop-info/v1/api/weather', reverse(
            'WeatherRecord'))
        response = self.client.get(
            '/weather-crop-info/v1/api/weather', {})
        self.assertEqual(response.status_code, 200)
        for record in response.data:
            self.assertEqual(record.get("station_id"), self.station_id)

    def test_weather_stats_api(self):
        """
            This method tests the WeatherStationStatsList view.

            Args:
                self.

            Returns:
                None
        """
        weather_record_file_handler(self.weather_record_file_name)
        self.assertEqual('/weather-crop-info/v1/api/weather/stats', reverse(
            'WeatherStationStats'))
        response = self.client.get(
            '/weather-crop-info/v1/api/weather/stats', {})
        self.assertEqual(response.status_code, 200)
        for record in response.data:
            self.assertEqual(record.get("station_id"), self.station_id)

    def tearDown(self):
        """
            This method is responsible for removing the setup that was created
            before execution of testcase. Invoked after every testcase.

            Args:
                self.

            Returns:
                None
        """
        os.remove("/tmp/USC00000072.txt")
