import uuid
from django.utils.functional import cached_property
from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from wagtail.models import Page
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField
from modelcluster.models import ClusterableModel
from datetime import datetime
from django.utils import timezone
# from Inlinepanel.edit_handlers import InlinePanel
from django.utils.text import slugify
from capeditor.utils import  paginate, query_param_to_list

from wagtail.admin.panels import MultiFieldPanel, FieldPanel, InlinePanel,FieldRowPanel
from capeditor.widgets import  BasemapPolygonWidget
        
            
# Create your models here.
class AlertList(Page):
    template = "capeditor/alert_index.html"
    ajax_template = 'capeditor/alert_list_include.html'

    subpage_types = [
        'capeditor.Alert',  # appname.ModelName
    ]
    parent_page_type = [
        'wagtailcore.Page'  # appname.ModelName
    ]
    max_count = 1

    alerts_per_page = models.PositiveIntegerField(default=6, validators=[
        MinValueValidator(6),
        MaxValueValidator(20),
    ], help_text="How many of this products should be visible on the landing page filter section ?")

    content_panels = Page.content_panels +[
        FieldPanel('alerts_per_page'),
    ]

    @property
    def filters(self):

        URGENCIES = {
            'Immediate':('Immediate'),
            'Expected':('Expected'),
            'Future':('Future'),
            'Past':('Past'),
            'Unknown':('Unknown'),
        }
        
        SEVERITIES = {
            'Extreme': ("Extreme - Extraordinary threat to life or property"),
            'Severe': ("Severe - Significant threat to life or property"),
            'Moderate': ("Moderate - Possible threat to life or property"),
            'Minor': ("Minor - Minimal to no known threat to life or property"),
            'Unknown': ("Unknown - Severity unknown"),
        }

        CERTAINTIES = {
            'Observed': ("Observed - Determined to have occurred or to be ongoing"),
            'Likely': ("Likely - Likely (percentage > ~50%)"),
            'Possible': ("Possible - Possible but not likely (percentage <= ~50%)"),
            'Unlikely': ("Unlikely - Not expected to occur (percentage ~ 0)"),
            'Unknown': ("Unknown - Certainty unknown"),
        }
        return {'urgency': URGENCIES, 'severity':SEVERITIES, 'certainty': CERTAINTIES}

    @property
    def all_alerts(self):
        return Alert.objects.live()

    def filter_alerts(self, request):
        alerts = self.all_alerts

        
        urgency = query_param_to_list(request.GET.get("urgency"), as_int=False)
        severity = query_param_to_list(request.GET.get("severity"), as_int=False)
        certainty = query_param_to_list(request.GET.get("certainty"), as_int=False)

        filters = models.Q()

        if urgency:
            filters &= models.Q(alert_info__urgency__in=urgency)
        if severity:
            filters &= models.Q(alert_info__severity__in=severity)
        if certainty:
            filters &= models.Q(alert_info__certainty__in=certainty)

        return alerts.filter(filters)

    def filter_and_paginate_alerts(self, request):
        page = request.GET.get('page')

        filtered_alerts = self.filter_alerts(request)

        paginated_alerts = paginate(filtered_alerts, page, self.alerts_per_page)

        return paginated_alerts


    def get_context(self, request, *args, **kwargs):
        context = super(AlertList,
                        self).get_context(request, *args, **kwargs)

        context['alerts'] = self.filter_and_paginate_alerts(request)
        context['latest_alert'] = self.all_alerts[0]

        return context
    

class Alert(Page):

    subpage_types = [
    ]
    parent_page_type = [
        'capeditor.AlertList'  # appname.ModelName
    ]

    template = "capeditor/alert_detail.html"

    STATUS_CHOICES = (
        ("Draft", "Draft - A preliminary template or draft, not actionable in its current form"),
        ("Actual", "Actual - Actionable by all targeted recipients"),
        ("Test", "Test - Technical testing only, all recipients disregard"),
        ("Exercise",
         "Exercise - Actionable only by designated exercise participants; exercise identifier SHOULD appear in note"),
        ("system", "System - For messages that support alert network internal functions"),
    )

    MESSAGE_TYPE_CHOICES = (
        ('Alert', "Alert - Initial information requiring attention by targeted recipients"),
        ('Update', "Update - Updates and supercedes the earlier message(s) identified in referenced alerts"),
        ('Cancel', "Cancel - Cancels the earlier message(s) identified in references"),
        ('Ack', "Acknowledge - Acknowledges receipt and acceptance of the message(s) identified in references field"),
        ('Error',
         "Error -  Indicates rejection of the message(s) identified in references; explanation SHOULD "
         "appear in note field"),
    )

    SCOPE_CHOICES = (
        ('Public', "Public - For general dissemination to unrestricted audiences"),
        ('Restricted',
         "Restricted - For dissemination only to users with a known operational requirement as in the restriction field"),
        ('Private', "Private - For dissemination only to specified addresses as in the addresses field in the alert"),
    )

  
    identifier = models.UUIDField(default=uuid.uuid4, editable=False,
                                  help_text="Unique ID. Auto generated on creation.")
    sender = models.EmailField(max_length=255,
                              help_text=" Identifies the originator of an alert. "
                                        "This can be an email of the institution for example", default='grace@gmail.com')
    sent = models.DateTimeField(help_text="Time and date of origination of the alert", default=timezone.now)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES,
                              help_text="The code denoting the appropriate handling of the alert", default='Actual')
    message_type = models.CharField(max_length=100, choices=MESSAGE_TYPE_CHOICES,
                                    help_text="The code denoting the nature of the alert message",  default='Alert')
    scope = models.CharField(max_length=100,
                             choices=SCOPE_CHOICES,
                             help_text="The code denoting the intended distribution of the alert message",  default='Public')
    source = models.TextField(blank=True, null=True, help_text="The text identifying the source of the alert message")
    restriction = models.TextField(blank=True, null=True,
                                   help_text="The text describing the rule for limiting distribution of the "
                                             "restricted alert message. Used when scope value is Restricted")
    code = models.CharField(max_length=100, blank=True, null=True,
                            help_text="The code denoting the special handling of the alert message")
    note = models.TextField(blank=True, null=True,
                            help_text="The text describing the purpose or significance of the alert message."
                                      "The message note is primarily intended for use with "
                                      "<status> 'Exercise' and <msgType> 'Error'")
                                                         
    content_panels = Page.content_panels + [

        MultiFieldPanel([
            FieldRowPanel([
            FieldPanel('sender'),
            FieldPanel('sent'),
            ]),
            FieldPanel('source'),
            
            FieldPanel('status',),
            FieldPanel('message_type', classname="message"),
            InlinePanel('references', heading="Earlier Reference Alerts -  If applicable", label="Alert", classname="references"),

            FieldPanel('note', classname='note'),

            FieldPanel('scope'),
            FieldPanel('restriction',classname="restriction" ),
            InlinePanel('addresses', heading="Intended Recipients (If scope is Private) ", label="Recipient", classname="addresses"),


        ], heading="Alert Identification (Sender, Message Type, Scope)"),

        MultiFieldPanel([
            InlinePanel('alert_info', label="Alert Information",  classname="collapsed")
        ], heading="Alert Info")
    ]

    subpage_types = [
        # 'capeditor.Alert',  # appname.ModelName
    ]
    parent_page_type = [
        'wagtailcore.Page'  # appname.ModelName
    ]

    


class AlertAddress(Orderable):
    alert = ParentalKey('Alert', related_name="addresses")
    name = models.TextField(help_text="Name of the recipient")
    address = models.EmailField(blank=True, null=True, help_text="Email")

    def __str__(self):
        return self.name


class AlertReference(Orderable):
    alert = ParentalKey('Alert', related_name='references')
    ref_alert = models.ForeignKey('Alert', blank=True, null=True, on_delete=models.PROTECT,
                                  help_text="Earlier alert referenced by this alert")

    def __str__(self):
        return f'{self.ref_alert.sender},{self.ref_alert.identifier},{self.ref_alert.sent}'
    
    @property
    def reference(self):
        return f'{self.ref_alert.sender},{self.ref_alert.identifier},{self.ref_alert.sent}'



class AlertIncident(Orderable):
    alert = ParentalKey('Alert', related_name='incidents', on_delete=models.CASCADE, )
    title = models.CharField(max_length=255, help_text="Title of the incident referent of the alert")
    description = models.TextField(help_text="Description of the incident")

    def __str__(self):
        return self.title

class AlertInfo(ClusterableModel):

    LANGUAGE_CHOICES = (
        ('en', "English"),
    )

    CATEGORY_CHOICES = (
        ('Geo', "Geophysical"),
        ('Met', "Meteorological"),
        ('Safety', "General emergency and public safety"),
        ('Security', "Law enforcement, military, homeland and local/private security"),
        ('Rescue', "Rescue and recovery"),
        ('Fire', "Fire suppression and rescue"),
        ('Health', "Medical and public health"),
        ('Env', "Pollution and other environmental"),
        ('Transport', "Public and private transportation"),
        ('Infra', "Utility, telecommunication, other non-transport infrastructure"),
        ('Cbrne', "Chemical, Biological, Radiological, Nuclear or High-Yield Explosive threat or attack"),
        ('Other', "Other events"),
    )

    URGENCY_CHOICES = (
        ('Immediate', "Immediate - Responsive action SHOULD be taken immediately"),
        ('Expected', "Expected - Responsive action SHOULD be taken soon (within next hour)"),
        ('Future', "Future - Responsive action SHOULD be taken in the near future"),
        ('Past', "Past - Responsive action is no longer required"),
        ('Unknown', "Unknown - Urgency not known"),
    )

    SEVERITY_CHOICES = (
        ('Extreme', "Extreme - Extraordinary threat to life or property"),
        ('Severe', "Severe - Significant threat to life or property"),
        ('Moderate', "Moderate - Possible threat to life or property"),
        ('Minor', "Minor - Minimal to no known threat to life or property"),
        ('Unknown', "Unknown - Severity unknown"),
    )

    CERTAINTY_CHOICES = (
        ('Observed', "Observed - Determined to have occurred or to be ongoing"),
        ('Likely', "Likely - Likely (percentage > ~50%)"),
        ('Possible', "Possible - Possible but not likely (percentage <= ~50%)"),
        ('Unlikely', "Unlikely - Not expected to occur (percentage ~ 0)"),
        ('Unknown', "Unknown - Certainty unknown"),
    )

    alert = ParentalKey('Alert', related_name="alert_info")

    language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES, default='en', blank=True, null=True,
                                help_text="The code denoting the language of the alert message")
    category = models.CharField(max_length=100,  default='Met',
                                choices=CATEGORY_CHOICES,
                                help_text="The code denoting the category of the subject event of the alert message")
    event = models.CharField(max_length=100,
                             help_text="The text denoting the type of the subject event of the alert message", blank=True, null=True)
    urgency = models.CharField(max_length=100,
                               choices=URGENCY_CHOICES,
                               help_text="The code denoting the urgency of the subject event of the alert message", default="Immediate")
    severity = models.CharField(max_length=100,
                                choices=SEVERITY_CHOICES,
                                help_text="The code denoting the severity of the subject event of the alert message", default="Extreme")
    certainty = models.CharField(max_length=100,
                                 choices=CERTAINTY_CHOICES,
                                 help_text="The code denoting the certainty of the subject event of the alert message", default="Likely")
    audience = models.TextField(blank=True, null=True,
                                help_text="The text describing the intended audience of the alert message")

    effective = models.DateTimeField(blank=True, null=True,
                                     help_text="The effective time of the information of the alert message")
    onset = models.DateTimeField(blank=True, null=True,
                                 help_text="The expected time of the beginning of the subject event "
                                           "of the alert message")
    expires = models.DateTimeField(blank=True, null=True,
                                   help_text="The expiry time of the information of the alert message")
    headline = models.TextField(blank=True, null=True, help_text="The text headline of the alert message")
    description = models.TextField(blank=True, null=True,
                                   help_text="The text describing the subject event of the alert message")
    instruction = models.TextField(blank=True, null=True,
                                   help_text="The text describing the recommended action to be taken by "
                                             "recipients of the alert message")
    web = models.URLField(blank=True, null=True,
                          help_text="The identifier of the hyperlink associating "
                                    "additional information with the alert message")
    contact = models.TextField(blank=True, null=True,
                               help_text="The text describing the contact for follow-up and "
                                         "confirmation of the alert message")

    
    panels = [

        MultiFieldPanel([
            FieldRowPanel([
            FieldPanel('language'),
            FieldPanel('event'),

            ]),
            FieldPanel('category'),
            FieldPanel('urgency'),
            FieldPanel('severity'),
            FieldPanel('certainty'),
            InlinePanel('response_types', heading="Response Types ", label="Response Type"),        
            FieldPanel('audience'),
            # FieldPanel('event_codes'),
            FieldRowPanel([
                FieldPanel('effective'),
                FieldPanel('onset'),
            ]),
            FieldPanel('expires'),

            
        ], heading="Alert Categorization (Category, Urgency, Severity, Certainity, Response & Dates)", classname="collapsed"),

        MultiFieldPanel([
            FieldPanel('headline'),
            FieldPanel('description'),
            FieldPanel('instruction'),

            FieldRowPanel([
                FieldPanel('web'),
                FieldPanel('contact'),
            ])
        ], heading ="Alert Delivery Message (Headline, Description, Intsructions, Contact & Website)", classname="collapsed"),


        MultiFieldPanel([
        InlinePanel('resources', heading="Alert Resources ", label="Resource"),
        ],  classname="collapsed"),

        MultiFieldPanel([
            InlinePanel('alert_areas',  heading="Alert Areas ",label="Alert Area"),
        ], classname="collapsed"),

        
    ]

    @property
    def is_expired(self):
        difference = (timezone.now() - self.expires).days
        if difference >= 0:
            return True
        return False


class AlertResponseType(Orderable):
    RESPONSE_TYPE_CHOICES = (
        ("Shelter", "Shelter - Take shelter in place or per instruction"),
        ("Evacuate", "Evacuate - Relocate as instructed in the instruction"),
        ("Prepare", "Prepare - Relocate as instructed in the instruction"),
        ("Execute", "Execute - Execute a pre-planned activity identified in instruction"),
        ("Avoid", "Avoid - Avoid the subject event as per the instruction"),
        ("Monitor", "Monitor - Attend to information sources as described in instruction"),
        ("Assess", "Assess - Evaluate the information in this message - DONT USE FOR PUBLIC ALERTS"),
        ("AllClear",
         "All Clear - The subject event no longer poses a threat or concern and any follow on action is described in instruction"),
        ("None", "No action recommended"),
    )

    alert = ParentalKey('AlertInfo', related_name='response_types', null=True)
    response_type = models.CharField(max_length=100, choices=RESPONSE_TYPE_CHOICES,
                                     help_text="The code denoting the type of action recommended for the "
                                               "target audience")

    def __str__(self) -> str:
        return self.response_type


class AlertResource(Orderable):
    alert_info = ParentalKey('AlertInfo', related_name='resources', null=True)
    resource_type = models.CharField(max_length=100, blank=True, null=True,
                                     help_text="Resource type whether is image, file etc")
    resource_desc = models.TextField(help_text="The text describing the type and content of the resource file")
    file = models.ForeignKey(
        'wagtaildocs.Document',
        help_text="File, Document etc",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    link = models.URLField(blank=True, null=True, help_text="The identifier of the hyperlink for the resource file")
    derefUri = models.TextField(blank=True, null=True,
                                help_text="The base-64 encoded data content of the resource file")
    digest = models.TextField(blank=True, null=True,
                              help_text="The code representing the digital digest ('hash') computed "
                                        "from the resource file")

    panels = [
        FieldPanel('resource_type'),
        FieldPanel('resource_desc'),
        FieldPanel('file'),
        FieldPanel('link'),
    ]

    @property
    def mime_type(self):
        return None


    @property
    def size(self):
        return None


class AlertArea(ClusterableModel):
    alert_info = ParentalKey('AlertInfo', related_name='alert_areas', null=True)
    area_desc = models.CharField(max_length=100, help_text="The text describing the affected area of the alert message",
                                 verbose_name="Affected areas / Regions",null=True)
   
    area = models.PolygonField(help_text="The paired values of points defining a polygon that delineates the affected "
                                         "area of the alert message", null=True, srid=4326)

    altitude = models.CharField(max_length=100,
                                blank=True,
                                null=True,
                                help_text="The specific or minimum altitude of the affected area of the alert message")
    ceiling = models.CharField(max_length=100,
                               blank=True,
                               null=True,
                               help_text="The maximum altitude of the affected area of the alert message."
                                         "MUST NOT be used except in combination with the altitude element. ") 
                          
    panels = [
        FieldPanel('area_desc'),
        FieldPanel('area', widget=BasemapPolygonWidget() ),
        InlinePanel('geocodes', label="Geocode", heading="Geocodes "),
        FieldPanel('altitude'),
        FieldPanel('ceiling'),
    ]   

class AlertEventCode(Orderable):
    alert_info = ParentalKey('AlertInfo', related_name='event_codes', null=True)
    name = models.CharField(max_length=100, help_text="Name for the event code")
    value = models.CharField(max_length=255, help_text="Value of the event code")


class AlertGeocode(Orderable):
    alert_info = ParentalKey('AlertArea', related_name='geocodes', null=True)
    name = models.CharField(max_length=100, help_text="Name for the geocode")
    value = models.CharField(max_length=255, help_text="Value of the geocode")
