"""
    This module contains url paths for weather_crop_info app. 
    
    Author: Chandrahas Reddy Mandapati 
"""
from django.urls import path

from . import views

urlpatterns = [
    path('v1/api/weather', views.WeatherRecordList.as_view(), name='WeatherRecord'),
    path('v1/api/weather/stats', views.WeatherStationStatsList.as_view(),
         name='WeatherStationStats'),
]
