from logging import getLogger

from django.apps import AppConfig
from django.conf import settings

from . import app_settings as defaults

config_logger = getLogger(__name__)


# Set some app default settings
for name in dir(defaults):
    if name.isupper() and not hasattr(settings, name):
        setattr(settings, name, getattr(defaults, name))


class NEMOAllauthConfig(AppConfig):
    name = "NEMO_allauth"
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        pass
