from django33.apps import AppConfig
from django33.contrib.staticfiles.checks import check_finders, check_storages
from django33.core import checks
from django33.utils.translation import gettext_lazy as _


class StaticFilesConfig(AppConfig):
    name = "django33.contrib.staticfiles"
    verbose_name = _("Static Files")
    ignore_patterns = ["CVS", ".*", "*~"]

    def ready(self):
        checks.register(check_finders, checks.Tags.staticfiles)
        checks.register(check_storages, checks.Tags.staticfiles)
