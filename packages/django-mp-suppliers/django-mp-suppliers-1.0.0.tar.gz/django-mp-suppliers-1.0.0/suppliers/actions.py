from django.contrib import messages
from django.utils.translation import gettext_lazy as _


def clean_products(modeladmin, request, queryset):
    for supplier in queryset:
        supplier.clean_products()

    messages.success(request, _("Prices cleaned"))


clean_products.short_description = _("Clean prices")
