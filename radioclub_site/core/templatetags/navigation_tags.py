from django import template

from wagtail.models import Page, Site

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    """Return the site root page for the current request."""
    return Site.find_for_request(context["request"]).root_page


@register.inclusion_tag("core/tags/main_menu.html", takes_context=True)
def main_menu(context, parent, calling_page=None):
    """Render the main navigation menu."""
    menuitems = parent.get_children().live().in_menu()
    return {
        "menuitems": menuitems,
        "calling_page": calling_page,
        "request": context["request"],
    }


@register.inclusion_tag("core/tags/footer_menu.html", takes_context=True)
def footer_menu(context, parent, calling_page=None):
    """Render the footer navigation menu."""
    menuitems = parent.get_children().live().in_menu()
    return {
        "menuitems": menuitems,
        "calling_page": calling_page,
        "request": context["request"],
    }
