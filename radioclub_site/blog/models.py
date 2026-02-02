from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "blog.BlogPage",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class BlogIndexPage(Page):
    """Lists all blog posts. Create one as a child of the homepage."""

    intro = RichTextField(
        blank=True,
        help_text="Introduction text displayed at the top of the blog listing.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    subpage_types = ["blog.BlogPage"]
    parent_page_types = ["home.HomePage"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        posts = (
            BlogPage.objects.live()
            .descendant_of(self)
            .order_by("-date")
        )

        tag = request.GET.get("tag")
        if tag:
            posts = posts.filter(tags__name=tag)

        context["posts"] = posts
        context["current_tag"] = tag
        return context


class BlogPage(Page):
    """An individual blog post."""

    date = models.DateField("Post date")
    intro = models.CharField(
        max_length=250,
        help_text="A short summary shown in the blog listing.",
    )
    body = RichTextField(help_text="The main content of the blog post.")
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Optional header image for the post.",
    )
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("tags"),
            ],
            heading="Post metadata",
        ),
        FieldPanel("header_image"),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    parent_page_types = ["blog.BlogIndexPage"]
    subpage_types = []
