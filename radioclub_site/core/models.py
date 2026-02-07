from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

from core.blocks import BaseStreamBlock


class BasePage(Page):
    """Abstract base page with common SEO fields."""

    class Meta:
        abstract = True
