from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from core.blocks import BaseStreamBlock


class ActivitiesIndexPage(Page):
    """Landing page that lists all activities grouped by type."""

    parent_page_types = ["home.HomePage"]
    subpage_types = [
        "activities.EventPage",
        "activities.ContestPage",
        "activities.DiplomaPage",
    ]
    max_count = 1

    introduction = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
    ]

    template = "activities/activities_index_page.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        children = self.get_children().live().public().specific()

        context["events"] = (
            children.type(EventPage).order_by("-eventpage__date_from")
        )
        context["contests"] = (
            children.type(ContestPage).order_by("-contestpage__date_from")
        )
        context["diplomas"] = children.type(DiplomaPage)

        return context

    class Meta:
        verbose_name = "Índice de actividades"


class EventPage(Page):
    """A single event organised by the radio club."""

    parent_page_types = ["activities.ActivitiesIndexPage"]
    subpage_types = []

    date_from = models.DateField("Fecha inicio")
    date_to = models.DateField("Fecha fin", blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    introduction = models.TextField(max_length=500, blank=True)
    body = StreamField(BaseStreamBlock(), blank=True, use_json_field=True)
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date_from"),
                FieldPanel("date_to"),
                FieldPanel("location"),
            ],
            heading="Detalles del evento",
        ),
        FieldPanel("introduction"),
        FieldPanel("header_image"),
        FieldPanel("body"),
    ]

    template = "activities/event_page.html"

    class Meta:
        verbose_name = "Evento"


class ContestPage(Page):
    """A radio contest with optional downloadable rules."""

    parent_page_types = ["activities.ActivitiesIndexPage"]
    subpage_types = []

    date_from = models.DateField("Fecha inicio")
    date_to = models.DateField("Fecha fin", blank=True, null=True)
    introduction = models.TextField(max_length=500, blank=True)
    body = StreamField(BaseStreamBlock(), blank=True, use_json_field=True)
    rules_document = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date_from"),
                FieldPanel("date_to"),
            ],
            heading="Fechas",
        ),
        FieldPanel("introduction"),
        FieldPanel("body"),
        FieldPanel("rules_document"),
    ]

    template = "activities/contest_page.html"

    class Meta:
        verbose_name = "Concurso"


class DiplomaPage(Page):
    """A diploma programme offered by the club."""

    parent_page_types = ["activities.ActivitiesIndexPage"]
    subpage_types = []

    introduction = models.TextField(max_length=500, blank=True)
    body = StreamField(BaseStreamBlock(), blank=True, use_json_field=True)
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("header_image"),
        FieldPanel("body"),
    ]

    template = "activities/diploma_page.html"

    class Meta:
        verbose_name = "Diploma"
