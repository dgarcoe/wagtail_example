from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from home.models import HomePage
from radio.models import RadioIndexPage, RadioPage


class RadioTests(WagtailPageTestCase):
    """Tests for the Radio section."""

    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(
            hostname="testsite", root_page=root_page, is_default_site=True
        )
        self.homepage = HomePage(title="Inicio")
        root_page.add_child(instance=self.homepage)

        self.radio_index = RadioIndexPage(title="Radio", slug="radio")
        self.homepage.add_child(instance=self.radio_index)

    def test_radio_index_is_renderable(self):
        self.assertPageIsRenderable(self.radio_index)

    def test_radio_page_creation_and_render(self):
        page = RadioPage(
            title="Satélites",
            slug="satelites",
            icon="bi-globe-americas",
            introduction="Info sobre satélites ham",
        )
        self.radio_index.add_child(instance=page)
        self.assertPageIsRenderable(page)

    def test_radio_page_allows_children(self):
        parent = RadioPage(title="VHF/UHF", slug="vhf-uhf")
        self.radio_index.add_child(instance=parent)
        child = RadioPage(title="Repetidores", slug="repetidores")
        parent.add_child(instance=child)
        self.assertTrue(RadioPage.objects.filter(slug="repetidores").exists())
