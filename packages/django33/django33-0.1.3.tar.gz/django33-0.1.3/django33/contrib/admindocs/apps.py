from django33.apps import AppConfig
from django33.utils.translation import gettext_lazy as _


class AdminDocsConfig(AppConfig):
    name = "django33.contrib.admindocs"
    verbose_name = _("Administrative Documentation")
