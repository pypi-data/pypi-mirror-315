from django33.apps import AppConfig
from django33.contrib.sites.checks import check_site_id
from django33.core import checks
from django33.db.models.signals import post_migrate
from django33.utils.translation import gettext_lazy as _

from .management import create_default_site


class SitesConfig(AppConfig):
    default_auto_field = "django33.db.models.AutoField"
    name = "django33.contrib.sites"
    verbose_name = _("Sites")

    def ready(self):
        post_migrate.connect(create_default_site, sender=self)
        checks.register(check_site_id, checks.Tags.sites)
