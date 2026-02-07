from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images import get_image_model_string

from core.blocks import BaseStreamBlock


class HomePage(Page):
    """Homepage for the radioclub website."""

    max_count = 1

    hero_title = models.CharField(
        "Título principal",
        max_length=255,
        blank=True,
        default="Unión de Radioaficionados de Vigo - Val Miñor",
    )
    hero_subtitle = models.CharField(
        "Subtítulo",
        max_length=255,
        blank=True,
        default="EA1RKV - Sección local de URE",
    )
    hero_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Imagen de portada",
    )
    hero_cta_text = models.CharField(
        "Texto del botón",
        max_length=50,
        blank=True,
        default="Conócenos",
    )
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Enlace del botón",
    )

    introduction = RichTextField("Introducción", blank=True)

    body = StreamField(
        BaseStreamBlock(),
        blank=True,
        use_json_field=True,
        verbose_name="Contenido",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                FieldPanel("hero_subtitle"),
                FieldPanel("hero_image"),
                FieldPanel("hero_cta_text"),
                FieldPanel("hero_cta_link"),
            ],
            heading="Sección Hero",
        ),
        FieldPanel("introduction"),
        FieldPanel("body"),
    ]

    subpage_types = [
        "about.AboutIndexPage",
        "blog.BlogIndexPage",
        "activities.ActivitiesIndexPage",
        "radio.RadioIndexPage",
        "contact.ContactPage",
        "gallery.GalleryIndexPage",
    ]

    class Meta:
        verbose_name = "Página de inicio"

    def get_context(self, request):
        context = super().get_context(request)
        # Get latest blog posts for homepage
        from blog.models import BlogPage
        context["latest_posts"] = (
            BlogPage.objects.live()
            .public()
            .order_by("-date")[:3]
        )
        # Get upcoming events
        from activities.models import EventPage
        from django.utils import timezone
        context["upcoming_events"] = (
            EventPage.objects.live()
            .public()
            .filter(date_from__gte=timezone.now().date())
            .order_by("date_from")[:3]
        )
        return context
