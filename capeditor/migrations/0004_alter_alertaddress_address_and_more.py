# Generated by Django 4.1.7 on 2023-04-04 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capeditor', '0003_alter_alertinfo_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alertaddress',
            name='address',
            field=models.EmailField(blank=True, help_text='Email', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='alertresponsetype',
            name='response_type',
            field=models.CharField(choices=[('Shelter', 'Shelter - Take shelter in place or per instruction'), ('Evacuate', 'Evacuate - Relocate as instructed in the instruction'), ('Prepare', 'Prepare - Relocate as instructed in the instruction'), ('Execute', 'Execute - Execute a pre-planned activity identified in instruction'), ('Avoid', 'Avoid - Avoid the subject event as per the instruction'), ('Monitor', 'Monitor - Attend to information sources as described in instruction'), ('Assess', 'Assess - Evaluate the information in this message - DONT USE FOR PUBLIC ALERTS'), ('AllClear', 'All Clear - The subject event no longer poses a threat or concern and any follow on action is described in instruction'), ('None', 'No action recommended')], help_text='The code denoting the type of action recommended for the target audience', max_length=100),
        ),
    ]
