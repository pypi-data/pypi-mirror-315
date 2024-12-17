from django33.apps import AppConfig
from django33.utils.translation import gettext_lazy as _


class RedirectsConfig(AppConfig):
    default_auto_field = "django33.db.models.AutoField"
    name = "django33.contrib.redirects"
    verbose_name = _("Redirects")
