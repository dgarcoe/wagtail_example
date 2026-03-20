from django.template.response import TemplateResponse

from wagtail.models import Page


def search(request):
    search_query = request.GET.get("query", "")
    if search_query:
        search_results = Page.objects.live().search(search_query)
    else:
        search_results = Page.objects.none()

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "search_results": search_results,
        },
    )
