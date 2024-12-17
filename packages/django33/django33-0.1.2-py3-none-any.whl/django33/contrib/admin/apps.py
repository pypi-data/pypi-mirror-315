from django33.apps import AppConfig
from django33.contrib.admin.checks import check_admin_app, check_dependencies
from django33.core import checks
from django33.utils.translation import gettext_lazy as _


class SimpleAdminConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    default_auto_field = "django33.db.models.AutoField"
    default_site = "django33.contrib.admin.sites.AdminSite"
    name = "django33.contrib.admin"
    verbose_name = _("Administration")

    def ready(self):
        checks.register(check_dependencies, checks.Tags.admin)
        checks.register(check_admin_app, checks.Tags.admin)


class AdminConfig(SimpleAdminConfig):
    """The default AppConfig for admin which does autodiscovery."""

    default = True

    def ready(self):
        super().ready()
        self.module.autodiscover()
