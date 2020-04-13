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
    audienceList = ('targetAudience1', 'targetAudience2', 'targetAudience3', 'targetAudience4')

    select_properties = (PageSelectProperty('level', 'Level', LEVEL_CHOICES),
                         PageSelectProperty('category', 'Cateory', CATEGORY_CHOICES),
                         PageSelectProperty('audience', 'Target Audience', YEAR_IN_SCHOOL_CHOICES, audienceList),
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
  
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]


class SearchableEvent:
    pass

class IdeaEventIndex(Page, RoutablePageMixin):
    subpage_types = ['TrainingEventsCollection', 'TrainTheTrainerEventsCollection']

    def get_context(self, request):
        context = super().get_context(request)
        children = filter_children(self, SearchableEvent)
        context['event_days'] = get_event_days(children)
        context['url'] = self.get_url(request)
        
        return context

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]


class IdeaTrainerIndex(Page, RoutablePageMixin):
    subpage_types = ['TrainerCollection']
    languageList = ('languagesSpoken1', 'languagesSpoken2', 'languagesSpoken3')
    select_properties = [PageSelectProperty('language', 'Language spoken', LANGUAGE_CHOICES, languageList)]
    query_properties = ('shortBio', 'firstName', 'lastName', 'country')

    def get_context(self, request):
        context = super().get_context(request)
        children = filter_children(self, Trainer)
        context['trainers'] = filter_pages(children, request, self.select_properties, self.query_properties)
        context['select_properties'] = self.select_properties
        context['url'] = self.get_url(request)
        return context

    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    


class PedagogyContent(Page, SearchableTrainingContent):
    category = models.CharField(default="Pedagogy", max_length=250)
    date = models.DateField("Training created", auto_now=True)
    targetAudience1 = models.CharField(choices=YEAR_IN_SCHOOL_CHOICES, max_length=250)
    targetAudience2 = models.CharField(choices=YEAR_IN_SCHOOL_CHOICES, max_length=250, blank=True)
    targetAudience3 = models.CharField(choices=YEAR_IN_SCHOOL_CHOICES, max_length=250, blank=True)
    targetAudience4 = models.CharField(choices=YEAR_IN_SCHOOL_CHOICES, max_length=250, blank=True)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=250)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=250)
    summary = models.CharField(max_length=3000)
    training = models.FileField(upload_to='trainings/',
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('level'),
        index.SearchField('category'),
        index.SearchField('language'),
        index.SearchField('summary')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('level'),
        FieldPanel('language'),
        FieldPanel('summary'),
        FieldPanel('training'),
        FieldPanel('targetAudience1'),
        FieldPanel('targetAudience2'),
        FieldPanel('targetAudience3'),
        FieldPanel('targetAudience4')

    ]

    def get_audiences(self):
        return filter(list(self.targetAudience1, self.targetAudience2, self.targetAudience3, self.targetAudience4))


class DebateContent(Page, SearchableTrainingContent):
    category = models.CharField(default="Debate", max_length=250)
    date = models.DateField("Training created", auto_now=True)
    targetAudience1 = models.CharField(choices=YEAR_IN_SCHOOL_CHOICES, max_length=250)
    targetAudience2 = models.CharField(choices=YEAR_IN_SCHOOL_CHOICES, max_length=250, blank=True)
    targetAudience3 = models.CharField(choices=YEAR_IN_SCHOOL_CHOICES, max_length=250, blank=True)
    targetAudience4 = models.CharField(choices=YEAR_IN_SCHOOL_CHOICES, max_length=250, blank=True)

    level = models.CharField(choices=LEVEL_CHOICES, max_length=250)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=250)
    summary = models.CharField(max_length=3000)
    training = models.FileField(upload_to='trainings/',
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('level'),
        index.SearchField('category'),
        index.SearchField('language'),
        index.SearchField('summary')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('level'),
        FieldPanel('language'),
        FieldPanel('summary'),
        FieldPanel('training'),
        FieldPanel('targetAudience1'),
        FieldPanel('targetAudience2'),
        FieldPanel('targetAudience3'),
        FieldPanel('targetAudience4')
    ]

    def get_audiences(self):
        return filter(list(self.targetAudience1, self.targetAudience2, self.targetAudience3, self.targetAudience4))


class TrainingContent(Page, SearchableTrainingContent):
    category = models.CharField(default="Training", max_length=250)
    date = models.DateField("Training created", auto_now=True)
    targetAudience1 = models.CharField(choices=YEAR_IN_SCHOOL_CHOICES, max_length=250)
    targetAudience2 = models.CharField(choices=YEAR_IN_SCHOOL_CHOICES, max_length=250, blank=True)
    targetAudience3 = models.CharField(choices=YEAR_IN_SCHOOL_CHOICES, max_length=250, blank=True)
    targetAudience4 = models.CharField(choices=YEAR_IN_SCHOOL_CHOICES, max_length=250, blank=True)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=250)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=250)
    summary = models.CharField(max_length=3000)
    training = models.FileField(upload_to='trainings/',
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    search_fields = Page.search_fields + [
        index.SearchField('level'),
        index.SearchField('category'),
        index.SearchField('language'),
        index.SearchField('summary'),
        FieldPanel('targetAudience1'),
        FieldPanel('targetAudience2'),
        FieldPanel('targetAudience3'),
        FieldPanel('targetAudience4')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('level'),
        FieldPanel('language'),
        FieldPanel('summary'),
        FieldPanel('training'),
        FieldPanel('targetAudience1'),
        FieldPanel('targetAudience2'),
        FieldPanel('targetAudience3'),
        FieldPanel('targetAudience4')

    ]

    def get_audiences(self):
        return filter(
            list(self.specific.targetAudience1, self.targetAudience2, self.targetAudience3, self.targetAudience4))


class Trainer(Page):
    profilePicture = models.ImageField(upload_to='trainers/',
                                       validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])])
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    languagesSpoken1 = models.CharField(choices=LANGUAGE_CHOICES, max_length=250)
    languagesSpoken2 = models.CharField(choices=LANGUAGE_CHOICES, max_length=250, blank=True)
    languagesSpoken3 = models.CharField(choices=LANGUAGE_CHOICES, max_length=250, blank=True)
    shortBio = models.CharField(max_length=3000)


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

    def get_languages(self):
        return filter(list(self.languagesSpoken1, self.languagesSpoken2, self.languagesSpoken3))


class TTTEvent(Page, SearchableEvent):
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
    typetraining = models.CharField("type of training", max_length=100, default="TTT")

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
        FieldPanel('trainer3')
    ]


class TrainingEvent(Page, SearchableEvent):
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
