from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Article, Service


class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return ["home", "about", "services", "projects", "blog", "careers", "faq", "contact"]

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return Service.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()


class ArticleSitemap(Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return Article.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_at

    def location(self, obj):
        return obj.get_absolute_url()


sitemaps = {
    "static": StaticViewSitemap,
    "services": ServiceSitemap,
    "articles": ArticleSitemap,
}
