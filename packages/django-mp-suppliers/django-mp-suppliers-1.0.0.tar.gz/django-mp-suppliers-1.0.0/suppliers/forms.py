from django import forms
from django.contrib.admin import TabularInline
from django.utils.translation import gettext_lazy as _
from django_select2.forms import Select2Widget

from suppliers.models import Supplier, SupplierWarehouse


class SupplierWarehouseInline(TabularInline):
    readonly_fields = ["price_updated"]
    model = SupplierWarehouse
    extra = 0
    max_num = 100


class SupplierChoiceWidget(Select2Widget):
    empty_label = _("Select supplier")


class SupplierChoiceField(forms.ModelChoiceField):
    def __init__(
        self,
        queryset=Supplier.objects.all(),
        required=False,
        widget=SupplierChoiceWidget(),
        *args,
        **kwargs
    ):
        super().__init__(
            queryset=queryset,
            required=required,
            widget=widget,
            *args,
            **kwargs
        )
