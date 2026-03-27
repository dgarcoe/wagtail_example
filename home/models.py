from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page


class HomePage(Page):
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Imagen de cabecera",
        help_text="Imagen panorámica que aparece debajo de la cabecera",
    )
    banner_title = models.CharField(
        max_length=255,
        default="EA1RKV",
        verbose_name="Título del banner",
    )
    banner_subtitle = models.CharField(
        max_length=255,
        default="Unión de Radioaficionados de Vigo-Val Miñor",
        blank=True,
        verbose_name="Subtítulo del banner",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("banner_image"),
                FieldPanel("banner_title"),
                FieldPanel("banner_subtitle"),
            ],
            heading="Banner de cabecera",
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
