from django.core.management.base import BaseCommand
from wagtail.models import Page, Site

from blog.models import BlogIndexPage
from home.models import HomePage


class Command(BaseCommand):
    help = "Create the BlogIndexPage and ensure it is reachable at /blog/"

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

        blog_index = BlogIndexPage.objects.first()

        if blog_index:
            # Fix slug/parent if needed (e.g. after removing i18n)
            moved = False
            if blog_index.slug != "blog":
                blog_index.slug = "blog"
                moved = True
            if blog_index.get_parent() != home:
                blog_index.move(home, pos="last-child")
                blog_index.refresh_from_db()
                moved = True
            if moved:
                blog_index.save()
                blog_index.save_revision().publish()
                self.stdout.write(self.style.SUCCESS("Fixed BlogIndexPage → /blog/"))
            else:
                self.stdout.write("BlogIndexPage already exists at /blog/")
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
