# Generated by Django 4.1.7 on 2023-02-20 18:58

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0078_referenceindex'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('identifier', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique ID. Auto generated on creation.')),
                ('sender', models.EmailField(help_text=' Identifies the originator of an alert. This can be an email of the institution for example', max_length=255)),
                ('sent', models.DateTimeField(help_text='Time and date of origination of the alert')),
                ('status', models.CharField(choices=[('draft', 'Draft - A preliminary template or draft, not actionable in its current form'), ('actual', 'Actual - Actionable by all targeted recipients'), ('test', 'Test - Technical testing only, all recipients disregard'), ('exercise', 'Exercise - Actionable only by designated exercise participants; exercise identifier SHOULD appear in note'), ('system', 'System - For messages that support alert network internal functions')], help_text='The code denoting the appropriate handling of the alert', max_length=50)),
                ('message_type', models.CharField(choices=[('alert', 'Alert - Initial information requiring attention by targeted recipients'), ('update', 'Update - Updates and supercedes the earlier message(s) identified in referenced alerts'), ('cancel', 'Cancel - Cancels the earlier message(s) identified in references'), ('ack', 'Acknowledge - Acknowledges receipt and acceptance of the message(s) identified in references field'), ('error', 'Error -  Indicates rejection of the message(s) identified in references; explanation SHOULD appear in note field')], help_text='The code denoting the nature of the alert message', max_length=100)),
                ('scope', models.CharField(choices=[('public', 'Public - For general dissemination to unrestricted audiences'), ('restricted', 'Restricted - For dissemination only to users with a known operational requirement as in the restriction field'), ('private', 'Private - For dissemination only to specified addresses as in the addresses field in the alert')], help_text='The code denoting the intended distribution of the alert message', max_length=100)),
                ('source', models.TextField(blank=True, help_text='The text identifying the source of the alert message', null=True)),
                ('restriction', models.TextField(blank=True, help_text='The text describing the rule for limiting distribution of the restricted alert message. Used when scope value is Restricted', null=True)),
                ('code', models.CharField(blank=True, help_text='The code denoting the special handling of the alert message', max_length=100, null=True)),
                ('note', models.TextField(blank=True, help_text="The text describing the purpose or significance of the alert message.The message note is primarily intended for use with <status> 'Exercise' and <msgType> 'Error'", null=True)),
                ('language', models.CharField(blank=True, choices=[('en', 'English')], default='en', help_text='The code denoting the language of the alert message', max_length=100, null=True)),
                ('category', models.CharField(choices=[('geo', 'Geophysical'), ('met', 'Meteorological'), ('safety', 'General emergency and public safety'), ('security', 'Law enforcement, military, homeland and local/private security'), ('rescue', 'Rescue and recovery'), ('fire', 'Fire suppression and rescue'), ('health', 'Medical and public health'), ('env', 'Pollution and other environmental'), ('transport', 'Public and private transportation'), ('infra', 'Utility, telecommunication, other non-transport infrastructure'), ('cbrne', 'Chemical, Biological, Radiological, Nuclear or High-Yield Explosive threat or attack'), ('other', 'Other events')], help_text='The code denoting the category of the subject event of the alert message', max_length=100)),
                ('event', models.CharField(help_text='The text denoting the type of the subject event of the alert message', max_length=100)),
                ('urgency', models.CharField(choices=[('immediate', 'Immediate - Responsive action SHOULD be taken immediately'), ('expected', 'Expected - Responsive action SHOULD be taken soon (within next hour)'), ('future', 'Future - Responsive action SHOULD be taken in the near future'), ('past', 'Past - Responsive action is no longer required'), ('unknown', 'Unknown - Urgency not known')], help_text='The code denoting the urgency of the subject event of the alert message', max_length=100)),
                ('severity', models.CharField(choices=[('extreme', 'Extreme - Extraordinary threat to life or property'), ('severe', 'Severe - Significant threat to life or property'), ('moderate', 'Moderate - Possible threat to life or property'), ('minor', 'Minor - Minimal to no known threat to life or property'), ('unknown', 'Unknown - Severity unknown')], help_text='The code denoting the severity of the subject event of the alert message', max_length=100)),
                ('certainty', models.CharField(choices=[('observed', 'Observed - Determined to have occurred or to be ongoing'), ('likely', 'Likely - Likely (percentage > ~50%)'), ('possible', 'Possible - Possible but not likely (percentage <= ~50%)'), ('unlikely', 'Unlikely - Not expected to occur (percentage ~ 0)'), ('unknown', 'Unknown - Certainty unknown')], help_text='The code denoting the certainty of the subject event of the alert message', max_length=100)),
                ('audience', models.TextField(blank=True, help_text='The text describing the intended audience of the alert message', null=True)),
                ('effective', models.DateTimeField(blank=True, help_text='The effective time of the information of the alert message', null=True)),
                ('onset', models.DateTimeField(blank=True, help_text='The expected time of the beginning of the subject event of the alert message', null=True)),
                ('expires', models.DateTimeField(blank=True, help_text='The expiry time of the information of the alert message', null=True)),
                ('headline', models.TextField(blank=True, help_text='The text headline of the alert message', null=True)),
                ('description', models.TextField(blank=True, help_text='The text describing the subject event of the alert message', null=True)),
                ('instruction', models.TextField(blank=True, help_text='The text describing the recommended action to be taken by recipients of the alert message', null=True)),
                ('web', models.URLField(blank=True, help_text='The identifier of the hyperlink associating additional information with the alert message', null=True)),
                ('contact', models.TextField(blank=True, help_text='The text describing the contact for follow-up and confirmation of the alert message', null=True)),
                ('area_desc', models.TextField(help_text='The text describing the affected area of the alert message', verbose_name='Affected areas / Regions')),
                ('altitude', models.CharField(blank=True, help_text='The specific or minimum altitude of the affected area of the alert message', max_length=100, null=True)),
                ('ceiling', models.CharField(blank=True, help_text='The maximum altitude of the affected area of the alert message.MUST NOT be used except in combination with the altitude element. ', max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
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
