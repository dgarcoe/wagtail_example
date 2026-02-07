from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from core.blocks import BaseStreamBlock


@register_snippet
class BoardMember(models.Model):
    """A member of the EA1RKV Vigo Val Miñor Radioclub (URV) board."""

    name = models.CharField(max_length=255)
    callsign = models.CharField(max_length=20, blank=True)
    role = models.CharField(
        max_length=255,
        help_text="Cargo en la junta directiva (e.g. Presidente, Secretario, Tesorero)",
    )
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    email = models.EmailField(blank=True)
    order = models.IntegerField(default=0)

    panels = [
        FieldPanel("name"),
        FieldPanel("callsign"),
        FieldPanel("role"),
        FieldPanel("photo"),
        FieldPanel("email"),
        FieldPanel("order"),
    ]

    class Meta:
        ordering = ["order"]

    def __str__(self):
        if self.callsign:
            return f"{self.callsign} - {self.name}"
        return self.name


class AboutIndexPage(Page):
    """Landing page for the 'About' section of the EA1RKV radioclub site."""

    parent_page_types = ["home.HomePage"]
    subpage_types = ["about.AboutPage"]
    max_count = 1
    template = "about/about_index_page.html"

    introduction = RichTextField(blank=True)
    body = StreamField(
        BaseStreamBlock(),
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("body"),
    ]

    def get_board_members(self):
        return BoardMember.objects.all()


class AboutPage(Page):
    """A generic sub-page under the About section."""

    parent_page_types = ["about.AboutIndexPage"]
    subpage_types = []
    template = "about/about_page.html"

    body = StreamField(
        BaseStreamBlock(),
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
