from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.core.fields import StreamField
from wagtail.core.blocks import ChoiceBlock
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.search import index

class IdeaTrainingIndex(RoutablePageMixin, Page):

    @route(r'^search/$')
    def post_search(self, request, *args, **kwargs):
        search_query = request.GET.get('q', None)
        self.children = self.children
        print(self)
        if search_query:
            self.children = self.children.filter(intro__contains=search_query)
            self.search_term = search_query
            self.search_type = 'search'
        return Page.serve(self, request, *args, **kwargs)
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

YEAR_IN_SCHOOL_CHOICES = [
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    ('SR', 'Senior'),
    ('GR', 'Graduate'),
]


class IdeaTraining(Page):
    date = models.DateField("Training created")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    doekmans = models.CharField(max_length=250)
    demo = models.CharField(choices=YEAR_IN_SCHOOL_CHOICES, max_length=250)


    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        FieldPanel('doekmans'),
        FieldPanel('demo')
    ]