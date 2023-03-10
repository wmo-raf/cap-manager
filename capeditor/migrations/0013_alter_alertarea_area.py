# Generated by Django 4.1.7 on 2023-02-23 08:06

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('capeditor', '0012_alter_alertarea_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alertarea',
            name='area',
            field=django.contrib.gis.db.models.fields.PolygonField(help_text='The paired values of points defining a polygon that delineates the affected area of the alert message', null=True, srid=4326),
        ),
    ]
