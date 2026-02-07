from datetime import date

from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from blog.models import BlogCategory, BlogIndexPage, BlogPage
from home.models import HomePage


class BlogTests(WagtailPageTestCase):
    """Tests for the Blog section."""

    def setUp(self):
        root_page = Page.get_first_root_node()
        Site.objects.create(
            hostname="testsite", root_page=root_page, is_default_site=True
        )
        self.homepage = HomePage(title="Inicio")
        root_page.add_child(instance=self.homepage)

        self.blog_index = BlogIndexPage(
            title="Noticias", slug="noticias"
        )
        self.homepage.add_child(instance=self.blog_index)

    def test_blog_index_is_renderable(self):
        self.assertPageIsRenderable(self.blog_index)

    def test_blog_page_creation(self):
        post = BlogPage(
            title="Test Post",
            slug="test-post",
            date=date.today(),
            introduction="A test post",
        )
        self.blog_index.add_child(instance=post)
        self.assertTrue(BlogPage.objects.filter(slug="test-post").exists())

    def test_blog_page_is_renderable(self):
        post = BlogPage(
            title="Test Post",
            slug="test-post",
            date=date.today(),
        )
        self.blog_index.add_child(instance=post)
        self.assertPageIsRenderable(post)

    def test_blog_category_creation(self):
        cat = BlogCategory.objects.create(name="Noticias", slug="noticias")
        self.assertEqual(str(cat), "Noticias")

    def test_blog_index_context_has_posts(self):
        post = BlogPage(title="Post", slug="post", date=date.today())
        self.blog_index.add_child(instance=post)
        response = self.client.get(self.blog_index.url)
        self.assertIn("posts", response.context)

    def test_blog_index_category_filter(self):
        cat = BlogCategory.objects.create(name="Test", slug="test")
        post = BlogPage(title="Post", slug="post", date=date.today())
        self.blog_index.add_child(instance=post)
        post.categories.add(cat)
        response = self.client.get(f"{self.blog_index.url}?category=test")
        self.assertEqual(response.status_code, 200)
