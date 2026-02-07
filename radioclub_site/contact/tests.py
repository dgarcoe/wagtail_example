from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from contact.models import ContactPage
from home.models import HomePage


class ContactTests(WagtailPageTestCase):
    """Tests for the Contact page."""

    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(
            hostname="testsite", root_page=root_page, is_default_site=True
        )
        self.homepage = HomePage(title="Inicio")
        root_page.add_child(instance=self.homepage)

        self.contact = ContactPage(
            title="Contacto",
            slug="contacto",
            introduction="<p>Contáctanos</p>",
            thank_you_text="<p>Gracias</p>",
        )
        self.homepage.add_child(instance=self.contact)

    def test_contact_page_is_renderable(self):
        self.assertPageIsRenderable(self.contact)

    def test_contact_page_template(self):
        response = self.client.get(self.contact.url)
        self.assertTemplateUsed(response, "contact/contact_page.html")
