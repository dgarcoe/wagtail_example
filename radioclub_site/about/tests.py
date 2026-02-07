from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from about.models import AboutIndexPage, AboutPage, BoardMember
from home.models import HomePage


class AboutPageTests(WagtailPageTestCase):
    """Tests for the About section pages."""

    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(
            hostname="testsite", root_page=root_page, is_default_site=True
        )
        self.homepage = HomePage(title="Inicio")
        root_page.add_child(instance=self.homepage)

        self.about_index = AboutIndexPage(
            title="Nosotros",
            slug="nosotros",
            introduction="<p>Sobre nosotros</p>",
        )
        self.homepage.add_child(instance=self.about_index)

    def test_about_index_is_renderable(self):
        self.assertPageIsRenderable(self.about_index)

    def test_about_page_creation(self):
        about_page = AboutPage(title="Historia", slug="historia")
        self.about_index.add_child(instance=about_page)
        self.assertTrue(AboutPage.objects.filter(slug="historia").exists())

    def test_about_page_is_renderable(self):
        about_page = AboutPage(title="Historia", slug="historia")
        self.about_index.add_child(instance=about_page)
        self.assertPageIsRenderable(about_page)

    def test_board_member_creation(self):
        member = BoardMember.objects.create(
            name="Test User", callsign="EA1TST", role="Presidente", order=1
        )
        self.assertEqual(str(member), "EA1TST - Test User")

    def test_board_member_without_callsign(self):
        member = BoardMember.objects.create(name="Test User", role="Vocal", order=2)
        self.assertEqual(str(member), "Test User")

    def test_about_index_get_board_members(self):
        BoardMember.objects.create(
            name="Test", callsign="EA1T", role="Presidente", order=1
        )
        members = self.about_index.get_board_members()
        self.assertEqual(members.count(), 1)
