# Generated by Django 4.1.7 on 2023-04-04 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('capeditor', '0004_alter_alertaddress_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alert',
            old_name='message_type',
            new_name='msgType',
        ),
        migrations.RenameField(
            model_name='alertarea',
            old_name='area_desc',
            new_name='areaDesc',
        ),
    ]
