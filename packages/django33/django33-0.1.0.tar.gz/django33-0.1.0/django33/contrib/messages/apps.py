from django33.apps import AppConfig
from django33.contrib.messages.storage import base
from django33.contrib.messages.utils import get_level_tags
from django33.core.signals import setting_changed
from django33.utils.functional import SimpleLazyObject
from django33.utils.translation import gettext_lazy as _


def update_level_tags(setting, **kwargs):
    if setting == "MESSAGE_TAGS":
        base.LEVEL_TAGS = SimpleLazyObject(get_level_tags)


class MessagesConfig(AppConfig):
    name = "django33.contrib.messages"
    verbose_name = _("Messages")

    def ready(self):
        setting_changed.connect(update_level_tags)
