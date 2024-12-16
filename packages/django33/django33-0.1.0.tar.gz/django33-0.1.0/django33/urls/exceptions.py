from django33.http import Http404


class Resolver404(Http404):
    pass


class NoReverseMatch(Exception):
    pass
