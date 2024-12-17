from django33.apps import AppConfig
from django33.contrib.contenttypes.checks import (
    check_generic_foreign_keys,
    check_model_name_lengths,
)
from django33.core import checks
from django33.db.models.signals import post_migrate, pre_migrate
from django33.utils.translation import gettext_lazy as _

from .management import create_contenttypes, inject_rename_contenttypes_operations


class ContentTypesConfig(AppConfig):
    default_auto_field = "django33.db.models.AutoField"
    name = "django33.contrib.contenttypes"
    verbose_name = _("Content Types")

    def ready(self):
        pre_migrate.connect(inject_rename_contenttypes_operations, sender=self)
        post_migrate.connect(create_contenttypes)
        checks.register(check_generic_foreign_keys, checks.Tags.models)
        checks.register(check_model_name_lengths, checks.Tags.models)
