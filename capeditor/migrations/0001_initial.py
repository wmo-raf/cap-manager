# Generated by Django 4.1.7 on 2023-03-25 13:21

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import modelcluster.fields
import uuid
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtaildocs', '0012_uploadeddocument'),
        ('wagtailcore', '0078_referenceindex'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('identifier', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique ID. Auto generated on creation.')),
                ('sender', models.EmailField(default='grace@gmail.com', help_text=' Identifies the originator of an alert. This can be an email of the institution for example', max_length=255)),
                ('sent', models.DateTimeField(default=django.utils.timezone.now, help_text='Time and date of origination of the alert')),
                ('status', models.CharField(choices=[('Draft', 'Draft - A preliminary template or draft, not actionable in its current form'), ('Actual', 'Actual - Actionable by all targeted recipients'), ('Test', 'Test - Technical testing only, all recipients disregard'), ('Exercise', 'Exercise - Actionable only by designated exercise participants; exercise identifier SHOULD appear in note'), ('system', 'System - For messages that support alert network internal functions')], default='Actual', help_text='The code denoting the appropriate handling of the alert', max_length=50)),
                ('message_type', models.CharField(choices=[('Alert', 'Alert - Initial information requiring attention by targeted recipients'), ('Update', 'Update - Updates and supercedes the earlier message(s) identified in referenced alerts'), ('Cancel', 'Cancel - Cancels the earlier message(s) identified in references'), ('Ack', 'Acknowledge - Acknowledges receipt and acceptance of the message(s) identified in references field'), ('Error', 'Error -  Indicates rejection of the message(s) identified in references; explanation SHOULD appear in note field')], default='Alert', help_text='The code denoting the nature of the alert message', max_length=100)),
                ('scope', models.CharField(choices=[('Public', 'Public - For general dissemination to unrestricted audiences'), ('Restricted', 'Restricted - For dissemination only to users with a known operational requirement as in the restriction field'), ('Private', 'Private - For dissemination only to specified addresses as in the addresses field in the alert')], default='Public', help_text='The code denoting the intended distribution of the alert message', max_length=100)),
                ('source', models.TextField(blank=True, help_text='The text identifying the source of the alert message', null=True)),
                ('restriction', models.TextField(blank=True, help_text='The text describing the rule for limiting distribution of the restricted alert message. Used when scope value is Restricted', null=True)),
                ('code', models.CharField(blank=True, help_text='The code denoting the special handling of the alert message', max_length=100, null=True)),
                ('note', models.TextField(blank=True, help_text="The text describing the purpose or significance of the alert message.The message note is primarily intended for use with <status> 'Exercise' and <msgType> 'Error'", null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='AlertArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_desc', models.CharField(help_text='The text describing the affected area of the alert message', max_length=100, null=True, verbose_name='Affected areas / Regions')),
                ('area', django.contrib.gis.db.models.fields.PolygonField(help_text='The paired values of points defining a polygon that delineates the affected area of the alert message', null=True, srid=4326)),
                ('altitude', models.CharField(blank=True, help_text='The specific or minimum altitude of the affected area of the alert message', max_length=100, null=True)),
                ('ceiling', models.CharField(blank=True, help_text='The maximum altitude of the affected area of the alert message.MUST NOT be used except in combination with the altitude element. ', max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AlertInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(blank=True, choices=[('en', 'English')], default='en', help_text='The code denoting the language of the alert message', max_length=100, null=True)),
                ('category', models.CharField(choices=[('Geo', 'Geophysical'), ('Met', 'Meteorological'), ('Safety', 'General emergency and public safety'), ('Security', 'Law enforcement, military, homeland and local/private security'), ('Rescue', 'Rescue and recovery'), ('Fire', 'Fire suppression and rescue'), ('Health', 'Medical and public health'), ('Env', 'Pollution and other environmental'), ('Transport', 'Public and private transportation'), ('Infra', 'Utility, telecommunication, other non-transport infrastructure'), ('Cbrne', 'Chemical, Biological, Radiological, Nuclear or High-Yield Explosive threat or attack'), ('Other', 'Other events')], default='Met', help_text='The code denoting the category of the subject event of the alert message', max_length=100)),
                ('event', models.CharField(blank=True, help_text='The text denoting the type of the subject event of the alert message', max_length=100, null=True)),
                ('urgency', models.CharField(choices=[('Immediate', 'Immediate - Responsive action SHOULD be taken immediately'), ('Expected', 'Expected - Responsive action SHOULD be taken soon (within next hour)'), ('Future', 'Future - Responsive action SHOULD be taken in the near future'), ('Past', 'Past - Responsive action is no longer required'), ('Unknown', 'Unknown - Urgency not known')], default='Immediate', help_text='The code denoting the urgency of the subject event of the alert message', max_length=100)),
                ('severity', models.CharField(choices=[('Extreme', 'Extreme - Extraordinary threat to life or property'), ('Severe', 'Severe - Significant threat to life or property'), ('Moderate', 'Moderate - Possible threat to life or property'), ('Minor', 'Minor - Minimal to no known threat to life or property'), ('Unknown', 'Unknown - Severity unknown')], default='Extreme', help_text='The code denoting the severity of the subject event of the alert message', max_length=100)),
                ('certainty', models.CharField(choices=[('Observed', 'Observed - Determined to have occurred or to be ongoing'), ('Likely', 'Likely - Likely (percentage > ~50%)'), ('Possible', 'Possible - Possible but not likely (percentage <= ~50%)'), ('Unlikely', 'Unlikely - Not expected to occur (percentage ~ 0)'), ('Unknown', 'Unknown - Certainty unknown')], default='Likely', help_text='The code denoting the certainty of the subject event of the alert message', max_length=100)),
                ('audience', models.TextField(blank=True, help_text='The text describing the intended audience of the alert message', null=True)),
                ('effective', models.DateTimeField(blank=True, help_text='The effective time of the information of the alert message', null=True)),
                ('onset', models.DateTimeField(blank=True, help_text='The expected time of the beginning of the subject event of the alert message', null=True)),
                ('expires', models.DateTimeField(blank=True, help_text='The expiry time of the information of the alert message', null=True)),
                ('headline', models.TextField(blank=True, help_text='The text headline of the alert message', null=True)),
                ('description', wagtail.fields.RichTextField(blank=True, help_text='The text describing the subject event of the alert message', null=True)),
                ('instruction', wagtail.fields.RichTextField(blank=True, help_text='The text describing the recommended action to be taken by recipients of the alert message', null=True)),
                ('web', models.URLField(blank=True, help_text='The identifier of the hyperlink associating additional information with the alert message', null=True)),
                ('contact', models.TextField(blank=True, help_text='The text describing the contact for follow-up and confirmation of the alert message', null=True)),
                ('alert', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='alert_info', to='capeditor.alert')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AlertList',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='AlertResponseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('response_type', models.CharField(choices=[('shelter', 'Shelter - Take shelter in place or per instruction'), ('evacuate', 'Evacuate - Relocate as instructed in the instruction'), ('prepare', 'Prepare - Relocate as instructed in the instruction'), ('execute', 'Execute - Execute a pre-planned activity identified in instruction'), ('avoid', 'Avoid - Avoid the subject event as per the instruction'), ('monitor', 'Monitor - Attend to information sources as described in instruction'), ('assess', 'Assess - Evaluate the information in this message - DONT USE FOR PUBLIC ALERTS'), ('all_clear', 'All Clear - The subject event no longer poses a threat or concern and any follow on action is described in instruction'), ('None', 'No action recommended')], help_text='The code denoting the type of action recommended for the target audience', max_length=100)),
                ('alert', modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='response_types', to='capeditor.alertinfo')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AlertResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('resource_type', models.CharField(blank=True, help_text='Resource type whether is image, file etc', max_length=100, null=True)),
                ('resource_desc', models.TextField(help_text='The text describing the type and content of the resource file')),
                ('link', models.URLField(blank=True, help_text='The identifier of the hyperlink for the resource file', null=True)),
                ('derefUri', models.TextField(blank=True, help_text='The base-64 encoded data content of the resource file', null=True)),
                ('digest', models.TextField(blank=True, help_text="The code representing the digital digest ('hash') computed from the resource file", null=True)),
                ('alert_info', modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='capeditor.alertinfo')),
                ('file', models.ForeignKey(blank=True, help_text='File, Document etc', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.document')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AlertReference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('alert', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='references', to='capeditor.alert')),
                ('ref_alert', models.ForeignKey(blank=True, help_text='Earlier alert referenced by this alert', null=True, on_delete=django.db.models.deletion.PROTECT, to='capeditor.alert')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AlertIncident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('title', models.CharField(help_text='Title of the incident referent of the alert', max_length=255)),
                ('description', models.TextField(help_text='Description of the incident')),
                ('alert', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='incidents', to='capeditor.alert')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AlertGeocode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.CharField(help_text='Name for the geocode', max_length=100)),
                ('value', models.CharField(help_text='Value of the geocode', max_length=255)),
                ('alert_info', modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='geocodes', to='capeditor.alertarea')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AlertEventCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.CharField(help_text='Name for the event code', max_length=100)),
                ('value', models.CharField(help_text='Value of the event code', max_length=255)),
                ('alert_info', modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_codes', to='capeditor.alertinfo')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='alertarea',
            name='alert_info',
            field=modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alert_areas', to='capeditor.alertinfo'),
        ),
        migrations.CreateModel(
            name='AlertAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('name', models.TextField(help_text='Name of the recipient')),
                ('address', models.TextField(blank=True, help_text='Address/Email/Contact', null=True)),
                ('alert', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='capeditor.alert')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]