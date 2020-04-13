from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class HomePage(Page):
    intro = RichTextField(blank=True)
    section_one_title = models.CharField(max_length=60, default="section_one_title")
    section_one_blurp = RichTextField(blank=True, default="section_one_blurp")
    section_one_link = models.CharField(max_length=60, default="section_one_link")
    section_two_title = models.CharField(max_length=60, default="section_two_title")
    section_two_blurp = RichTextField(blank=True, default="section_two_blurp")
    section_two_link = models.CharField(max_length=60, default="section_two_link")
    section_three_title = models.CharField(max_length=60, default="section_three_title")
    section_three_blurp = RichTextField(blank=True, default="section_three_blurp")
    section_three_link = models.CharField(max_length=60, default="section_three_link")

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('section_one_title', classname="full"),
        FieldPanel('section_one_blurp', classname="full"),
        FieldPanel('section_one_link', classname="full"),
        FieldPanel('section_two_title', classname="full"),
        FieldPanel('section_two_blurp', classname="full"),
        FieldPanel('section_two_link', classname="full"),
        FieldPanel('section_three_title', classname="full"),
        FieldPanel('section_three_blurp', classname="full"),
        FieldPanel('section_three_link', classname="full"),
    ]
