from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.search import index

from trainingandtrainers.utils import *


class TrainingEventsCollection(Page):
    subpage_types = ['TrainingEvent']


class TrainTheTrainerEventsCollection(Page):
    subpage_types = ['TTTEvent']


class TrainingContentCollection(Page):
    subpage_types = ['TrainingContent']


class PedagogyContentCollection(Page):
    subpage_types = ['PedagogyContent']


class DebateContentCollection(Page):
    subpage_types = ['DebateContent']


class TrainerCollection(Page):
    subpage_types = ['Trainer']


YEAR_IN_SCHOOL_CHOICES = [
    ('primary', 'Primary Education'),
    ('secondary', 'Secondary Education'),
    ('tertiary', 'Tertiary Education'),
    ('adult', 'Adult Education')
]

LEVEL_CHOICES = [
    ('1', 'Beginner'),
    ('2', 'Intermediate'),
    ('3', 'Advanced')
]

LANGUAGE_CHOICES = [
    ('English', 'English'),
    ('Dutch', 'Dutch'),
    ('German', 'German'),
    ('Slovak', 'Slovak'),
    ('Estionian', 'Estonian'),
    ('Latvian', 'Latvian'),
    ('Romanian', 'Romanian'),
    ('Macedonian', 'Macedonian')
]

CATEGORY_CHOICES = [
    ('Training', 'Training'),
    ('Debate', 'Debate Content'),
    ('Pedagogy', 'Pedagogy Content'),
]

TRAININGEVENT_CHOICES = [
    ('Training', 'Training'),
    ('TTT', 'Train-the-Trainer')
]


class SearchableTrainingContent:
    pass


class IdeaTrainingIndex(Page, RoutablePageMixin):
    subpage_types = ['TrainingContentCollection', 'PedagogyContentCollection', 'DebateContentCollection']
    select_properties = (PageSelectProperty('level', 'Level', LEVEL_CHOICES),
                         PageSelectProperty('category', 'Cateory', CATEGORY_CHOICES),
                         PageSelectProperty('targetAudience', 'Target Audience', YEAR_IN_SCHOOL_CHOICES),
                         PageSelectProperty('language', 'Language', LANGUAGE_CHOICES))
    query_properties = ('summary', 'title')

    def get_context(self, request):
        context = super().get_context(request)
        children = filter_children(self, SearchableTrainingContent)
        context['select_properties'] = self.select_properties
        context['trainings'] = filter_pages(children, request, self.select_properties, self.query_properties)
        context['url'] = self.get_url(request)
        return context

    intro = RichTextField(blank=True)


class IdeaEventIndex(Page, RoutablePageMixin):
    subpage_types = ['TrainingEventsCollection', 'TrainTheTrainerEventsCollection']
    select_properties = (PageSelectProperty('typeTraining', 'training Type', TRAININGEVENT_CHOICES))
    query_properties = ('title', 'date', 'city', 'country', 'trainer1', 'trainer2', 'trainer3')

    def get_context(self, request):
        context = super().get_context(request)
        events = TrainingEvent.objects.all()
        context['events'] = events
        context['url'] = self.get_url(request)
        return context

    intro = RichTextField(blank=True)


class IdeaTrainerIndex(Page, RoutablePageMixin):
    subpage_types = ['TrainerCollection']
    languageList = ('languagesSpoken1', 'languagesSpoken2', 'languagesSpoken3')
    select_properties = (PageSelectProperty(languageList, 'Language spoken', LANGUAGE_CHOICES))
    query_properties = ('shortBio', 'name', 'country')

    def get_context(self, request):
        context = super().get_context(request)
        trainers = TrainingEvent.objects.all()
        context['trainers'] = trainers
        context['url'] = self.get_url(request)
        return context

    intro = RichTextField(blank=True)


class PedagogyContent(Page, SearchableTrainingContent):
    category = models.CharField(default="Pedagogy", max_length=250)
    date = models.DateField("Training created", auto_now=True)
    targetAudience = models.CharField(choices=YEAR_IN_SCHOOL_CHOICES, max_length=250)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=250)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=250)
    summary = models.CharField(max_length=3000)
    training = models.FileField(upload_to='trainings/',
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('targetAudience'),
        index.SearchField('level'),
        index.SearchField('category'),
        index.SearchField('language'),
        index.SearchField('summary')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('targetAudience'),
        FieldPanel('level'),
        FieldPanel('language'),
        FieldPanel('summary'),
        FieldPanel('training')

    ]


class DebateContent(Page, SearchableTrainingContent):
    category = models.CharField(default="Debate", max_length=250)
    date = models.DateField("Training created", auto_now=True)
    targetAudience = models.CharField(choices=YEAR_IN_SCHOOL_CHOICES, max_length=250)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=250)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=250)
    summary = models.CharField(max_length=3000)
    training = models.FileField(upload_to='trainings/',
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('targetAudience'),
        index.SearchField('level'),
        index.SearchField('category'),
        index.SearchField('language'),
        index.SearchField('summary')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('targetAudience'),
        FieldPanel('level'),
        FieldPanel('language'),
        FieldPanel('summary'),
        FieldPanel('training')

    ]


class TrainingContent(Page, SearchableTrainingContent):
    category = models.CharField(default="Training", max_length=250)
    date = models.DateField("Training created", auto_now=True)
    targetAudience = models.CharField(choices=YEAR_IN_SCHOOL_CHOICES, max_length=250)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=250)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=250)
    summary = models.CharField(max_length=3000)
    training = models.FileField(upload_to='trainings/',
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    search_fields = Page.search_fields + [
        index.SearchField('targetAudience'),
        index.SearchField('level'),
        index.SearchField('category'),
        index.SearchField('language'),
        index.SearchField('summary')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('targetAudience'),
        FieldPanel('level'),
        FieldPanel('language'),
        FieldPanel('summary'),
        FieldPanel('training')

    ]


class Trainer(Page):
    profilePicture = models.ImageField(upload_to='trainers/',
                                       validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])])
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    # languagesSpoken = models.MultiSelectField(choices=LANGUAGE_CHOICES, max_length=250)
    languagesSpoken1 = models.CharField(choices=LANGUAGE_CHOICES, max_length=250)
    languagesSpoken2 = models.CharField(choices=LANGUAGE_CHOICES, max_length=250, blank=True)
    languagesSpoken3 = models.CharField(choices=LANGUAGE_CHOICES, max_length=250, blank=True)
    shortBio = models.CharField(max_length=3000)
    # python alreadyExists = models.IntegerField(default=0)

    search_fields = Page.search_fields + [
        index.SearchField('firstName'),
        index.SearchField('lastName'),
        index.SearchField('country'),
        index.SearchField('languagesSpoken1'),
        index.SearchField('languagesSpoken2'),
        index.SearchField('languagesSpoken3')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('profilePicture'),
        FieldPanel('firstName'),
        FieldPanel('lastName'),
        FieldPanel('age'),
        FieldPanel('city'),
        FieldPanel('country'),
        FieldPanel('shortBio'),
        FieldPanel('languagesSpoken1'),
        FieldPanel('languagesSpoken2'),
        FieldPanel('languagesSpoken3')
    ]

    def save(self, *args, **kwargs):
        self.title = self.firstName + ' ' + self.lastName
        siblings = self.get_siblings(inclusive=False)
        for sibling in siblings:
            if sibling.owner == self.owner:
                raise ValidationError(ValidationError('Invalid value'))
        super().save(*args, **kwargs)


class TTTEvent(Page):
    date = models.DateTimeField("date and time of event")
    street = models.CharField("Street and number", max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    contactemail = models.CharField("Contact Emailadresss", max_length=100, blank=True)
    contactwebsite = models.CharField("Contact website", max_length=100, blank=True)
    description = models.CharField(max_length=3000)
    trainer1 = models.CharField(max_length=100, default="")
    trainer2 = models.CharField(max_length=100, blank=True)
    trainer3 = models.CharField(max_length=100, blank=True)
    typetraining = models.CharField("type of training", max_length=100, blank=True, choices=TRAININGEVENT_CHOICES)

    search_fields = Page.search_fields + [
        index.SearchField('date'),
        index.SearchField('city'),
        index.SearchField('country'),
        index.SearchField('trainer1'),
        index.SearchField('trainer2'),
        index.SearchField('trainer3'),
        index.SearchField('typetraining')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('street'),
        FieldPanel('city'),
        FieldPanel('country'),
        FieldPanel('contactemail'),
        FieldPanel('contactwebsite'),
        FieldPanel('description'),
        FieldPanel('trainer1'),
        FieldPanel('trainer2'),
        FieldPanel('trainer3'),
        FieldPanel('typetraining')
    ]


class TrainingEvent(Page):
    Title = models.CharField(max_length=100)
    date = models.DateTimeField("date and time of event")
    street = models.CharField("Street and number", max_length=100, default="")
    city = models.CharField(max_length=100, default="")
    country = models.CharField(max_length=100, default="")
    contactemail = models.CharField("Contact Emailadresss", max_length=100, blank=True)
    contactwebsite = models.CharField("Contact website", max_length=100, blank=True)
    description = models.CharField(max_length=3000, default="")
    trainer1 = models.CharField(max_length=100, default="")
    trainer2 = models.CharField(max_length=100, blank=True)
    trainer3 = models.CharField(max_length=100, blank=True)
    typetraining = models.CharField("type of training", max_length=100, blank=True, default='Training')

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('date'),
        index.SearchField('city'),
        index.SearchField('country'),
        index.SearchField('trainer1'),
        index.SearchField('trainer2'),
        index.SearchField('trainer3'),
        index.SearchField('typetraining')
    ]

    content_panels = Page.content_panels + [
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


class BlankNewPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]
