from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.core.fields import StreamField
from wagtail.core.blocks import ChoiceBlock
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index
from django.core.validators import FileExtensionValidator



YEAR_IN_SCHOOL_CHOICES = [
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    ('SR', 'Senior'),
    ('GR', 'Graduate'),
]

LEVEL_CHOICES = [
    ('1',   '1'),
    ('2',   '2'),
    ('3',   '3'),
    ('4',   '4'),
    ('5',   '5'),
]

LANGUAGE_CHOICES = [
    ('English',     'English'),
    ('Dutch',       'Dutch'),
    ('German',      'German'),
    ('Slovak',      'Slovak'),
    ('Estionian',   'Estonian'),
    ('Latvian',     'Latvian'),
    ('Romanian',    'Romanian'),
    ('Macedonian',  'Macedonian')
]

CATEGORY_CHOICES = [
    ('Training',    'Training'),
    ('Debate',      'Debate Content'),
    ('Pedagogy',    'Pedagogy Content'),
]

class IdeaTrainingIndex(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]




class IdeaTraining(Page):
    date = models.DateField("Training created", auto_now = True)
    subject = models.CharField(max_length=100)
    targetAudience = models.CharField(choices=YEAR_IN_SCHOOL_CHOICES, max_length=250)
    level =  models.CharField(choices=LEVEL_CHOICES, max_length=250)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=250)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=250)
    summary = models.CharField(max_length=3000)
    training = models.FileField(upload_to='trainings/',
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])])


    search_fields = Page.search_fields + [
        index.SearchField('subject'),
        index.SearchField('targetAudience'),
        index.SearchField('level'),
        index.SearchField('category'),
        index.SearchField('language')


    ]

    content_panels = Page.content_panels + [
        #FieldPanel('date'),
        FieldPanel('subject'),
        FieldPanel('targetAudience'),
        FieldPanel('level'),
        FieldPanel('language'),
        FieldPanel('category'),
        FieldPanel('summary'),
        FieldPanel('training')

    ]


class Trainer(Page):
    profilePicture = models.ImageField(upload_to='trainers/',
                                validators=[FileExtensionValidator(allowed_extensions=['jpg','png,'])])
    #date = models.DateField("Training created", auto_now = True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    city =  models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    #languagesSpoken = models.MultiSelectField(choices=LANGUAGE_CHOICES, max_length=250)
    shortBio = models.CharField(max_length=3000)

    search_fields = Page.search_fields + [
        index.SearchField('name'),
        index.SearchField('country')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('profilePicture'),
        FieldPanel('name'),
        FieldPanel('age'),
        FieldPanel('city'),
        FieldPanel('country'),
        FieldPanel('shortBio'),
    ]


class TrainingEvent(Page):
    Title = models.CharField(max_length=100)
    date = models.DateTimeField("date and time of event")
    street = models.CharField("Street and number",max_length=100)
    city =  models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    contactemail = models.CharField("Contact Emailadresss",max_length=100,blank=True)
    contactwebsite = models.CharField("Contact website",max_length=100,blank=True)
    description = models.CharField(max_length=3000)
    trainer1 = models.CharField(max_length=100)
    trainer2 = models.CharField(max_length=100,blank=True)
    trainer3 = models.CharField(max_length=100,blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('date'),
        index.SearchField('city'),
        index.SearchField('country'),
        index.SearchField('trainer1'),
        index.SearchField('trainer2'),
        index.SearchField('trainer3')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('title'),
        FieldPanel('date'),
        FieldPanel('street'),
        FieldPanel('city'),
        FieldPanel('country'),
        FieldPanel('contactemail'),
        FieldPanel('contactwebsite'),
        FieldPanel('description'),
        FieldPanel('trainer1'),
        FieldPanel('trainer2'),
        FieldPanel('trainer3')

    ]


    
