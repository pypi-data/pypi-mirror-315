from django33.apps import apps as django_apps
from django33.contrib.sitemaps import Sitemap
from django33.core.exceptions import ImproperlyConfigured


class FlatPageSitemap(Sitemap):
    def items(self):
        if not django_apps.is_installed("django33.contrib.sites"):
            raise ImproperlyConfigured(
                "FlatPageSitemap requires django33.contrib.sites, which isn't installed."
            )
        Site = django_apps.get_model("sites.Site")
        current_site = Site.objects.get_current()
        return current_site.flatpage_set.filter(registration_required=False)
