"""
Management command to seed initial data for the EA1RKV radioclub website.

Creates the basic page structure and a superuser for development.
Idempotent: safe to run multiple times.
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from wagtail.models import Page, Site

from about.models import AboutIndexPage, AboutPage, BoardMember
from activities.models import ActivitiesIndexPage
from blog.models import BlogIndexPage
from contact.models import ContactPage
from gallery.models import GalleryIndexPage
from home.models import HomePage
from radio.models import RadioIndexPage, RadioPage


User = get_user_model()


class Command(BaseCommand):
    help = "Seed initial page structure and data for the EA1RKV radioclub site."

    def handle(self, *args, **options):
        self._create_superuser()
        homepage = self._ensure_homepage()
        self._create_section_pages(homepage)
        self._create_board_members()
        self.stdout.write(self.style.SUCCESS("Initial data seeded successfully."))

    def _create_superuser(self):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@ea1rkv.es",
                password="admin",
            )
            self.stdout.write(self.style.SUCCESS("Created superuser: admin / admin"))
        else:
            self.stdout.write("Superuser 'admin' already exists.")

    def _ensure_homepage(self):
        """Ensure a proper HomePage exists as the site root."""
        try:
            return HomePage.objects.get(depth=2)
        except HomePage.DoesNotExist:
            pass

        root = Page.objects.get(depth=1)
        # Remove default Wagtail welcome page if present
        Page.objects.filter(depth=2, slug="home").exclude(
            pk__in=HomePage.objects.values_list("pk", flat=True)
        ).delete()

        homepage = HomePage(
            title="Inicio",
            slug="home",
            hero_title="Unión de Radioaficionados de Vigo - Val Miñor",
            hero_subtitle="EA1RKV - Sección local de URE",
            hero_cta_text="Conócenos",
            introduction=(
                "<p>Bienvenidos a la web de la Unión de Radioaficionados de Vigo - Val Miñor "
                "(EA1RKV), sección local de la <strong>Unión de Radioaficionados Españoles "
                "(URE)</strong> en Vigo, Pontevedra.</p>"
                "<p>Nos reunimos el primer viernes de cada mes a las 20:00h en nuestra sede "
                "social. Si te interesa la radioafición, ¡ven a conocernos!</p>"
            ),
            show_in_menus=True,
        )
        root.add_child(instance=homepage)

        Site.objects.update_or_create(
            is_default_site=True,
            defaults={
                "hostname": "localhost",
                "port": 8000,
                "root_page": homepage,
                "site_name": "URV EA1RKV",
            },
        )
        self.stdout.write(self.style.SUCCESS("Created HomePage."))
        return homepage

    def _create_section_pages(self, homepage):
        """Create the main section pages under the homepage."""
        sections = [
            {
                "model": AboutIndexPage,
                "slug": "nosotros",
                "title": "Nosotros",
                "kwargs": {
                    "introduction": (
                        "<p>Somos la sección local de la URE en Vigo y Val Miñor. "
                        "Nuestro indicativo es <strong>EA1RKV</strong>.</p>"
                    ),
                },
            },
            {
                "model": BlogIndexPage,
                "slug": "noticias",
                "title": "Noticias",
                "kwargs": {
                    "introduction": (
                        "<p>Últimas noticias y artículos del radioclub.</p>"
                    ),
                },
            },
            {
                "model": ActivitiesIndexPage,
                "slug": "actividades",
                "title": "Actividades",
                "kwargs": {
                    "introduction": (
                        "<p>Concursos, diplomas y eventos organizados por el radioclub.</p>"
                    ),
                },
            },
            {
                "model": RadioIndexPage,
                "slug": "radio",
                "title": "Radio",
                "kwargs": {
                    "introduction": (
                        "<p>Recursos técnicos sobre radioafición: satélites, "
                        "HF, VHF/UHF, APRS, meteorología y más.</p>"
                    ),
                },
            },
            {
                "model": GalleryIndexPage,
                "slug": "galeria",
                "title": "Galería",
                "kwargs": {
                    "introduction": (
                        "<p>Fotos de nuestras actividades y eventos.</p>"
                    ),
                },
            },
            {
                "model": ContactPage,
                "slug": "contacto",
                "title": "Contacto",
                "kwargs": {
                    "introduction": (
                        "<p>¿Tienes alguna pregunta? Ponte en contacto con nosotros.</p>"
                    ),
                    "thank_you_text": (
                        "<p>Gracias por tu mensaje. Te responderemos lo antes posible.</p>"
                    ),
                    "to_address": "seccion.vigo@ure.es",
                    "from_address": "web@ea1rkv.es",
                    "subject": "Mensaje desde la web EA1RKV",
                },
            },
        ]

        for section in sections:
            model = section["model"]
            if not model.objects.filter(slug=section["slug"]).exists():
                page = model(
                    title=section["title"],
                    slug=section["slug"],
                    show_in_menus=True,
                    **section["kwargs"],
                )
                homepage.add_child(instance=page)
                self.stdout.write(f"  Created: {section['title']}")

        # Create radio sub-pages
        self._create_radio_pages()
        # Create about sub-pages
        self._create_about_pages()

    def _create_radio_pages(self):
        """Create technical radio sub-pages."""
        try:
            radio_index = RadioIndexPage.objects.get(slug="radio")
        except RadioIndexPage.DoesNotExist:
            return

        radio_topics = [
            {
                "slug": "satelites",
                "title": "Satélites",
                "icon": "bi-globe-americas",
                "introduction": (
                    "Información sobre satélites de radioaficionado (Ham Sats), "
                    "software de seguimiento orbital y comunicaciones vía satélite."
                ),
            },
            {
                "slug": "meteo",
                "title": "Satélites Meteorológicos",
                "icon": "bi-cloud-sun",
                "introduction": (
                    "Recepción de imágenes de satélites meteorológicos NOAA, "
                    "Meteor M2 y otros. Tratamiento de señal APT y LRPT."
                ),
            },
            {
                "slug": "hf",
                "title": "HF - Onda Corta",
                "icon": "bi-broadcast",
                "introduction": (
                    "Comunicaciones en bandas de HF (1.8 - 30 MHz). "
                    "Modos: SSB, CW, FT8, RTTY y digitales."
                ),
            },
            {
                "slug": "vhf-uhf",
                "title": "VHF / UHF",
                "icon": "bi-broadcast-pin",
                "introduction": (
                    "Actividad en bandas de VHF (144 MHz) y UHF (430 MHz). "
                    "Repetidores locales y comunicaciones en FM y SSB."
                ),
            },
            {
                "slug": "aprs",
                "title": "APRS",
                "icon": "bi-pin-map",
                "introduction": (
                    "Sistema Automático de Reporte de Posición (APRS). "
                    "Seguimiento de estaciones, meteorología y mensajería."
                ),
            },
        ]

        for topic in radio_topics:
            if not RadioPage.objects.filter(slug=topic["slug"]).exists():
                page = RadioPage(
                    title=topic["title"],
                    slug=topic["slug"],
                    icon=topic["icon"],
                    introduction=topic["introduction"],
                    show_in_menus=True,
                )
                radio_index.add_child(instance=page)
                self.stdout.write(f"    Created radio page: {topic['title']}")

    def _create_about_pages(self):
        """Create about sub-pages."""
        try:
            about_index = AboutIndexPage.objects.get(slug="nosotros")
        except AboutIndexPage.DoesNotExist:
            return

        about_pages = [
            {
                "slug": "historia",
                "title": "Historia del Club",
            },
            {
                "slug": "sede",
                "title": "Nuestra Sede",
            },
        ]

        for page_data in about_pages:
            if not AboutPage.objects.filter(slug=page_data["slug"]).exists():
                page = AboutPage(
                    title=page_data["title"],
                    slug=page_data["slug"],
                    show_in_menus=True,
                )
                about_index.add_child(instance=page)
                self.stdout.write(f"    Created about page: {page_data['title']}")

    def _create_board_members(self):
        """Create initial board members."""
        members = [
            {"name": "Chus De Prado", "callsign": "EA1IQ", "role": "Presidente", "order": 1},
        ]

        for member_data in members:
            BoardMember.objects.get_or_create(
                callsign=member_data["callsign"],
                defaults=member_data,
            )
        self.stdout.write(self.style.SUCCESS("Board members seeded."))
