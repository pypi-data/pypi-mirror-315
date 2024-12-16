from django33.middleware.csrf import get_token
from django33.utils.functional import lazy
from django33.utils.html import format_html
from django33.utils.safestring import SafeString


def csrf_input(request):
    return format_html(
        '<input type="hidden" name="csrfmiddlewaretoken" value="{}">',
        get_token(request),
    )


csrf_input_lazy = lazy(csrf_input, SafeString, str)
csrf_token_lazy = lazy(get_token, str)
