from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from suppliers.actions import clean_products
from suppliers.forms import SupplierWarehouseInline
from suppliers.models import Supplier


@admin.register(Supplier)
class SupplierAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "short_name",
        "code",
        "currency",
        "discount",
        "markup",
        "is_visible_for_unregistered_users",
        "country",
        "warehouse_count",
        "price_updated",
    ]

    list_display_links = ["id", "name"]

    list_editable = ["is_visible_for_unregistered_users"]

    actions = [clean_products]

    inlines = [SupplierWarehouseInline]
