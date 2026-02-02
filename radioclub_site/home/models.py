from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class HomePage(Page):

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        from blog.models import BlogPage

        from blog.models import BlogIndexPage

        blog_index = BlogIndexPage.objects.live().descendant_of(self).first()
        context["blog_index"] = blog_index
        context["latest_posts"] = (
            BlogPage.objects.live().descendant_of(self).order_by("-date")[:3]
        )
        return context
    # Hero section
    banner_title = models.CharField(
        max_length=255,
        blank=True,
        default="Welcome to the Radio Club",
        help_text="Main heading displayed in the hero section.",
    )
    banner_subtitle = models.CharField(
        max_length=255,
        blank=True,
        default="Connecting amateur radio enthusiasts since day one",
        help_text="Subtitle displayed below the main heading.",
    )
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Optional hero/banner image.",
    )

    # About section
    about_title = models.CharField(
        max_length=255,
        blank=True,
        default="About Our Club",
    )
    about_description = RichTextField(
        blank=True,
        default=(
            "We are a community of amateur radio operators dedicated to advancing "
            "the art, science, and practice of radio communication. Whether you are "
            "a seasoned ham or just getting started, you are welcome here."
        ),
        help_text="Description of the radio club.",
    )

    # Activities section
    activities_title = models.CharField(
        max_length=255,
        blank=True,
        default="Our Activities",
    )
    activity_1_title = models.CharField(
        max_length=100, blank=True, default="HF & VHF Operating"
    )
    activity_1_description = models.TextField(
        blank=True,
        default=(
            "Regular on-air activity across HF and VHF bands, including nets, "
            "ragchewing, and DX contacts around the world."
        ),
    )
    activity_2_title = models.CharField(
        max_length=100, blank=True, default="Contests & Field Day"
    )
    activity_2_description = models.TextField(
        blank=True,
        default=(
            "We participate in major contests and ARRL Field Day, setting up "
            "portable stations and operating around the clock."
        ),
    )
    activity_3_title = models.CharField(
        max_length=100, blank=True, default="Training & Licensing"
    )
    activity_3_description = models.TextField(
        blank=True,
        default=(
            "We offer study sessions and exam preparation for Technician, General, "
            "and Amateur Extra license classes."
        ),
    )
    activity_4_title = models.CharField(
        max_length=100, blank=True, default="Emergency Communications"
    )
    activity_4_description = models.TextField(
        blank=True,
        default=(
            "Our members train in emergency communications and support local "
            "agencies through ARES and RACES programs."
        ),
    )

    # Meeting info section
    meeting_title = models.CharField(
        max_length=255,
        blank=True,
        default="Meetings & Events",
    )
    meeting_description = RichTextField(
        blank=True,
        default=(
            "We meet on the first Thursday of each month at 7:00 PM. "
            "All meetings are open to the public — bring a friend!"
        ),
        help_text="Information about club meetings and events.",
    )

    # Contact section
    contact_title = models.CharField(
        max_length=255,
        blank=True,
        default="Get In Touch",
    )
    contact_email = models.EmailField(
        blank=True,
        default="info@radioclub.example.com",
    )
    contact_description = RichTextField(
        blank=True,
        default=(
            "Interested in joining or have questions? Reach out to us and "
            "we will be happy to help you get started in amateur radio."
        ),
    )
    club_callsign = models.CharField(
        max_length=20,
        blank=True,
        help_text="The club's amateur radio callsign (e.g. W1AW).",
    )
    repeater_info = models.CharField(
        max_length=255,
        blank=True,
        help_text="Club repeater frequency and details (e.g. 146.940 MHz, -600 kHz offset, PL 100.0).",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("banner_title"),
                FieldPanel("banner_subtitle"),
                FieldPanel("banner_image"),
            ],
            heading="Hero Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("about_title"),
                FieldPanel("about_description"),
            ],
            heading="About Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("activities_title"),
                FieldPanel("activity_1_title"),
                FieldPanel("activity_1_description"),
                FieldPanel("activity_2_title"),
                FieldPanel("activity_2_description"),
                FieldPanel("activity_3_title"),
                FieldPanel("activity_3_description"),
                FieldPanel("activity_4_title"),
                FieldPanel("activity_4_description"),
            ],
            heading="Activities Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("meeting_title"),
                FieldPanel("meeting_description"),
            ],
            heading="Meetings Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("contact_title"),
                FieldPanel("contact_email"),
                FieldPanel("contact_description"),
                FieldPanel("club_callsign"),
                FieldPanel("repeater_info"),
            ],
            heading="Contact Section",
        ),
    ]
