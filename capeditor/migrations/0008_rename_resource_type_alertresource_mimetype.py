# Generated by Django 4.1.7 on 2023-04-04 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('capeditor', '0007_alertresource_size'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alertresource',
            old_name='resource_type',
            new_name='mimeType',
        ),
    ]