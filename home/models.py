from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class HomePage(Page):
    hero_title = models.CharField(
        max_length=255,
        default="EA1RKV",
        verbose_name="Hero title",
    )
    hero_subtitle = models.CharField(
        max_length=255,
        default="Unión de Radioaficionados de Vigo-Val Miñor",
        verbose_name="Hero subtitle",
    )
    hero_cta_text = models.CharField(
        max_length=50,
        blank=True,
        default="Ver Blog",
        verbose_name="Call to action text",
    )
    hero_cta_link = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Call to action link",
        help_text="Relative URL, e.g. /blog/",
    )

    club_description = RichTextField(
        blank=True,
        verbose_name="Club description",
    )
    club_callsign = models.CharField(
        max_length=20,
        default="EA1RKV",
        verbose_name="Club callsign",
    )
    club_frequency = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Club frequency",
        help_text="e.g. 145.550 MHz",
    )
    club_locator = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="QTH Locator",
        help_text="e.g. IN52JD",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                FieldPanel("hero_subtitle"),
                FieldPanel("hero_cta_text"),
                FieldPanel("hero_cta_link"),
            ],
            heading="Hero Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("club_description"),
                FieldPanel("club_callsign"),
                FieldPanel("club_frequency"),
                FieldPanel("club_locator"),
            ],
            heading="Club Information",
        ),
    ]

    max_count = 1
    subpage_types = ["blog.BlogIndexPage"]

    def get_context(self, request):
        from blog.models import BlogPage

        context = super().get_context(request)
        context["latest_posts"] = (
            BlogPage.objects.live().public().order_by("-first_published_at")[:6]
        )
        return context

    class Meta:
        verbose_name = "Home Page"
