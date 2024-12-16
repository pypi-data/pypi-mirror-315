from django33.contrib.gis.geos.error import GEOSException
from django33.contrib.gis.ptr import CPointerBase


class GEOSBase(CPointerBase):
    null_ptr_exception_class = GEOSException
