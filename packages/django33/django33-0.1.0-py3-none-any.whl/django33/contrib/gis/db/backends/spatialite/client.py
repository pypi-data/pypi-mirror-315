from django33.db.backends.sqlite3.client import DatabaseClient


class SpatiaLiteClient(DatabaseClient):
    executable_name = "spatialite"
