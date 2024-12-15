from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SuppliersAppConfig(AppConfig):
    name = "suppliers"
    verbose_name = _("Suppliers")


default_app_config = "suppliers.SuppliersAppConfig"
