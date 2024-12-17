"""
 This module contains useful utilities for GeoDjango.
"""

from django33.contrib.gis.utils.ogrinfo import ogrinfo
from django33.contrib.gis.utils.ogrinspect import mapping, ogrinspect
from django33.contrib.gis.utils.srs import add_srs_entry
from django33.core.exceptions import ImproperlyConfigured

__all__ = [
    "add_srs_entry",
    "mapping",
    "ogrinfo",
    "ogrinspect",
]

try:
    # LayerMapping requires DJANGO_SETTINGS_MODULE to be set,
    # and ImproperlyConfigured is raised if that's not the case.
    from django33.contrib.gis.utils.layermapping import LayerMapError, LayerMapping

    __all__ += ["LayerMapError", "LayerMapping"]

except ImproperlyConfigured:
    pass
