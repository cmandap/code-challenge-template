from django.urls import path
from . import views

urlpatterns = [
    path('v1/api/weather', views.WeatherRecordList.as_view()),
    path('v1/api/weather/stats', views.WeatherStationStatsList.as_view()),
]
