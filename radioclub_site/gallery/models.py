from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.images import get_image_model_string


class GalleryIndexPage(Page):
    """Index page listing all photo galleries."""

    parent_page_types = ["home.HomePage"]
    subpage_types = ["gallery.GalleryPage"]
    max_count = 1

    introduction = RichTextField("Introducción", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
    ]

    template = "gallery/gallery_index_page.html"

    class Meta:
        verbose_name = "Índice de galerías"


class GalleryPage(Page):
    """A photo gallery/album page."""

    parent_page_types = ["gallery.GalleryIndexPage"]
    subpage_types = []

    date = models.DateField("Fecha", blank=True, null=True)
    introduction = models.TextField("Descripción", max_length=500, blank=True)
    cover_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Imagen de portada",
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("introduction"),
        FieldPanel("cover_image"),
        InlinePanel("gallery_images", label="Imágenes"),
    ]

    template = "gallery/gallery_page.html"

    class Meta:
        verbose_name = "Galería de fotos"


class GalleryImage(Orderable):
    """An image within a gallery."""

    page = ParentalKey(GalleryPage, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.CASCADE,
        related_name="+",
    )
    caption = models.CharField("Pie de foto", max_length=255, blank=True)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "Imagen de galería"
