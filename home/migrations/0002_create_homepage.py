from django.db import migrations


def create_homepage(apps, schema_editor):
    ContentType = apps.get_model("contenttypes.ContentType")
    Page = apps.get_model("wagtailcore.Page")
    Site = apps.get_model("wagtailcore.Site")
    HomePage = apps.get_model("home.HomePage")
    Locale = apps.get_model("wagtailcore.Locale")

    # Get or create the default locale
    locale, _ = Locale.objects.get_or_create(language_code="es")

    # Create the HomePage content type
    homepage_ct, _ = ContentType.objects.get_or_create(
        model="homepage", app_label="home"
    )

    # Get the root page
    root_page = Page.objects.get(depth=1)

    # Delete the default Wagtail welcome page if it exists
    Page.objects.filter(depth=2).delete()

    # Create the homepage using treebeard path conventions
    homepage = HomePage.objects.create(
        title="EA1RKV - Radioclub Vigo-Val Miñor",
        slug="home",
        content_type=homepage_ct,
        locale=locale,
        path=root_page.path + "0001",
        depth=2,
        numchild=0,
        hero_title="EA1RKV",
        hero_subtitle="Unión de Radioaficionados de Vigo-Val Miñor",
        hero_cta_text="Ver Blog",
        hero_cta_link="/es/blog/",
        club_callsign="EA1RKV",
        club_frequency="145.550 MHz",
        club_locator="IN52JD",
        club_description="<p>Club de radioaficionados de Vigo y Val Miñor, Galicia.</p>",
    )

    # Update root page's numchild
    root_page.numchild = 1
    root_page.save()

    # Create the default site pointing to the homepage
    Site.objects.all().delete()
    Site.objects.create(
        hostname="localhost",
        port=8000,
        root_page=homepage,
        is_default_site=True,
        site_name="EA1RKV",
    )


def remove_homepage(apps, schema_editor):
    Page = apps.get_model("wagtailcore.Page")
    # Just delete depth-2 pages (homepage)
    Page.objects.filter(depth=2).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
        ("wagtailcore", "0094_alter_page_locale"),
    ]

    operations = [
        migrations.RunPython(create_homepage, remove_homepage),
    ]
