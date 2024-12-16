from django33.contrib.gis.gdal.error import GDALException
from django33.contrib.gis.ptr import CPointerBase


class GDALBase(CPointerBase):
    null_ptr_exception_class = GDALException
