from datetime import date

from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from activities.models import ActivitiesIndexPage, ContestPage, DiplomaPage, EventPage
from home.models import HomePage


class ActivitiesTests(WagtailPageTestCase):
    """Tests for the Activities section."""

    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(
            hostname="testsite", root_page=root_page, is_default_site=True
        )
        self.homepage = HomePage(title="Inicio")
        root_page.add_child(instance=self.homepage)

        self.activities_index = ActivitiesIndexPage(
            title="Actividades", slug="actividades"
        )
        self.homepage.add_child(instance=self.activities_index)

    def test_activities_index_is_renderable(self):
        self.assertPageIsRenderable(self.activities_index)

    def test_event_page_creation_and_render(self):
        event = EventPage(
            title="Field Day",
            slug="field-day",
            date_from=date(2026, 6, 1),
            location="Monte da Mina",
        )
        self.activities_index.add_child(instance=event)
        self.assertPageIsRenderable(event)

    def test_contest_page_creation_and_render(self):
        contest = ContestPage(
            title="Diploma Xacobeo",
            slug="diploma-xacobeo",
            date_from=date(2026, 1, 1),
        )
        self.activities_index.add_child(instance=contest)
        self.assertPageIsRenderable(contest)

    def test_diploma_page_creation_and_render(self):
        diploma = DiplomaPage(
            title="Diploma Galicia",
            slug="diploma-galicia",
        )
        self.activities_index.add_child(instance=diploma)
        self.assertPageIsRenderable(diploma)

    def test_activities_index_context(self):
        event = EventPage(
            title="Event", slug="event", date_from=date(2026, 6, 1)
        )
        self.activities_index.add_child(instance=event)
        response = self.client.get(self.activities_index.url)
        self.assertIn("events", response.context)
        self.assertIn("contests", response.context)
        self.assertIn("diplomas", response.context)
