from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ManagersAppConfig(AppConfig):
    name = "managers"
    verbose_name = _("Managers")


default_app_config = "managers.ManagersAppConfig"
