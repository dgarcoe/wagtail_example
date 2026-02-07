from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from gallery.models import GalleryIndexPage, GalleryPage
from home.models import HomePage


class GalleryTests(WagtailPageTestCase):
    """Tests for the Gallery section."""

    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(
            hostname="testsite", root_page=root_page, is_default_site=True
        )
        self.homepage = HomePage(title="Inicio")
        root_page.add_child(instance=self.homepage)

        self.gallery_index = GalleryIndexPage(title="Galería", slug="galeria")
        self.homepage.add_child(instance=self.gallery_index)

    def test_gallery_index_is_renderable(self):
        self.assertPageIsRenderable(self.gallery_index)

    def test_gallery_page_creation_and_render(self):
        gallery = GalleryPage(
            title="Field Day 2026",
            slug="field-day-2026",
            introduction="Fotos del Field Day",
        )
        self.gallery_index.add_child(instance=gallery)
        self.assertPageIsRenderable(gallery)
