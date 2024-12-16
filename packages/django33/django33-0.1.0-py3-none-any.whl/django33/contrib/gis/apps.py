from django33.apps import AppConfig
from django33.core import serializers
from django33.utils.translation import gettext_lazy as _


class GISConfig(AppConfig):
    default_auto_field = "django33.db.models.AutoField"
    name = "django33.contrib.gis"
    verbose_name = _("GIS")

    def ready(self):
        serializers.BUILTIN_SERIALIZERS.setdefault(
            "geojson", "django33.contrib.gis.serializers.geojson"
        )
