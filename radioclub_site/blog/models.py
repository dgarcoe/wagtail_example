from datetime import date

from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models

from modelcluster.fields import ParentalManyToManyField

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from core.blocks import BaseStreamBlock


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categorías"


class BlogIndexPage(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["blog.BlogPage"]
    max_count = 1

    introduction = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
    ]

    template = "blog/blog_index_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = (
            BlogPage.objects.live()
            .descendant_of(self)
            .order_by("-first_published_at")
        )

        current_category = request.GET.get("category")
        if current_category:
            blogpages = blogpages.filter(categories__slug=current_category)

        paginator = Paginator(blogpages, 9)
        page_number = request.GET.get("page")
        try:
            posts = paginator.page(page_number)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context["posts"] = posts
        context["categories"] = BlogCategory.objects.all()
        context["current_category"] = current_category
        return context


class BlogPage(Page):
    parent_page_types = ["blog.BlogIndexPage"]
    subpage_types = []

    date = models.DateField("Fecha de publicación", default=date.today)
    introduction = models.TextField(
        max_length=500, blank=True, help_text="Resumen del artículo"
    )
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField(
        BaseStreamBlock(),
        blank=True,
        use_json_field=True,
    )
    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
            ],
            heading="Información del artículo",
        ),
        FieldPanel("introduction"),
        FieldPanel("header_image"),
        FieldPanel("body"),
    ]

    template = "blog/blog_page.html"
