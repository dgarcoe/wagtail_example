from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from home.models import HomePage


class HomePageTests(WagtailPageTestCase):
    """Tests for the HomePage model."""

    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(
            hostname="testsite", root_page=root_page, is_default_site=True
        )
        self.homepage = HomePage(
            title="Inicio",
            hero_title="Test Radioclub",
            hero_subtitle="EA1RKV",
        )
        root_page.add_child(instance=self.homepage)

    def test_homepage_creation(self):
        self.assertTrue(HomePage.objects.filter(title="Inicio").exists())

    def test_homepage_is_renderable(self):
        self.assertPageIsRenderable(self.homepage)

    def test_homepage_template_used(self):
        response = self.client.get(self.homepage.url)
        self.assertTemplateUsed(response, "home/home_page.html")

    def test_homepage_hero_fields(self):
        self.assertEqual(self.homepage.hero_title, "Test Radioclub")
        self.assertEqual(self.homepage.hero_subtitle, "EA1RKV")

    def test_homepage_context_has_latest_posts(self):
        response = self.client.get(self.homepage.url)
        self.assertIn("latest_posts", response.context)

    def test_homepage_context_has_upcoming_events(self):
        response = self.client.get(self.homepage.url)
        self.assertIn("upcoming_events", response.context)
