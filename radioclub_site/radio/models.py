from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from core.blocks import BaseStreamBlock


class RadioIndexPage(Page):
    """
    Página índice que lista todas las secciones técnicas de radio
    del club EA1RKV: satélites, imagen meteorológica, HF/VHF/UHF,
    concursos, etc.
    """

    parent_page_types = ["home.HomePage"]
    subpage_types = ["radio.RadioPage"]
    max_count = 1

    introduction = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
    ]

    template = "radio/radio_index_page.html"

    class Meta:
        verbose_name = "Sección Radio"


class RadioPage(Page):
    """
    Página de contenido técnico de radio. Permite anidamiento para
    crear jerarquías (e.g., Satélites > NOAA > APT).
    """

    parent_page_types = ["radio.RadioIndexPage"]
    subpage_types = ["radio.RadioPage"]

    icon = models.CharField(
        max_length=50,
        blank=True,
        default="bi-broadcast",
        help_text="Clase de icono Bootstrap Icons (e.g., bi-broadcast, bi-globe, bi-cloud-sun)",
    )
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
        FieldPanel("icon"),
        FieldPanel("introduction"),
        FieldPanel("header_image"),
        FieldPanel("body"),
    ]

    template = "radio/radio_page.html"

    class Meta:
        verbose_name = "Página técnica de radio"
