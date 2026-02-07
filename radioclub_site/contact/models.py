from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.fields import RichTextField


class FormField(AbstractFormField):
    page = ParentalKey("ContactPage", on_delete=models.CASCADE, related_name="form_fields")


class ContactPage(AbstractEmailForm):
    """Contact page with built-in form builder and club info."""

    parent_page_types = ["home.HomePage"]
    subpage_types = []
    max_count = 1

    introduction = RichTextField("Introducción", blank=True)
    thank_you_text = RichTextField("Texto de agradecimiento", blank=True)

    # Map embed for location
    map_url = models.URLField(
        "URL del mapa (Google Maps embed)",
        blank=True,
        help_text="URL de inserción de Google Maps para mostrar la ubicación de la sede",
    )

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("introduction"),
        InlinePanel("form_fields", label="Campos del formulario"),
        FieldPanel("thank_you_text"),
        FieldPanel("map_url"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Configuración de email",
        ),
    ]

    template = "contact/contact_page.html"
    landing_page_template = "contact/contact_page_landing.html"

    class Meta:
        verbose_name = "Página de contacto"
