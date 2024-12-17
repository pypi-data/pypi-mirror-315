# RemovedInDjango60Warning: Remove this entire module.

import warnings

from django33.utils.deprecation import RemovedInDjango60Warning


def is_iterable(x):
    "An implementation independent way of checking for iterables"
    warnings.warn(
        "django33.utils.itercompat.is_iterable() is deprecated. "
        "Use isinstance(..., collections.abc.Iterable) instead.",
        RemovedInDjango60Warning,
        stacklevel=2,
    )
    try:
        iter(x)
    except TypeError:
        return False
    else:
        return True
