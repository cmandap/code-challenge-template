# Generated by Django 4.1.6 on 2023-02-10 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather_crop_info', '0002_remove_weatherrecord_unique_station_date_constraint_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weatherrecord',
            name='weather_station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather_crop_info.weatherstation', verbose_name='Application Generated Station Reference'),
        ),
        migrations.AlterField(
            model_name='weatherstationstats',
            name='weather_station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather_crop_info.weatherstation', verbose_name='Application Generated Station Reference'),
        ),
    ]
