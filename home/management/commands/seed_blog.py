from django.core.management.base import BaseCommand
from wagtail.models import Page, Site

from blog.models import BlogIndexPage, BlogPage
from home.models import HomePage


class Command(BaseCommand):
    help = "Create the BlogIndexPage if it doesn't exist"

    def handle(self, *args, **options):
        # Ensure we have a HomePage as site root
        try:
            home = HomePage.objects.get()
        except HomePage.DoesNotExist:
            self.stdout.write(self.style.WARNING("No HomePage found — skipping blog seed"))
            return

        # Ensure the Site root is set to HomePage
        site = Site.objects.filter(is_default_site=True).first()
        if site and site.root_page_id != home.pk:
            site.root_page = home
            site.save()
            self.stdout.write("Fixed default site root → HomePage")

        # Create BlogIndexPage if missing
        if BlogIndexPage.objects.exists():
            self.stdout.write("BlogIndexPage already exists — skipping")
            return

        blog_index = BlogIndexPage(
            title="Blog",
            slug="blog",
            intro="",
            live=True,
        )
        home.add_child(instance=blog_index)
        blog_index.save_revision().publish()
        self.stdout.write(self.style.SUCCESS("Created BlogIndexPage at /blog/"))
