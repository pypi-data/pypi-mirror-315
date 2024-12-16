from django33.apps import AppConfig
from django33.utils.translation import gettext_lazy as _


class SyndicationConfig(AppConfig):
    name = "django33.contrib.syndication"
    verbose_name = _("Syndication")
