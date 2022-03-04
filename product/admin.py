from django.contrib import admin
from .models import Product
from import_export.admin import ImportExportModelAdmin

from .resources import ProductResources


class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResources
    list_display = ('serial_no', 'part_no', 'is_emi', 'is_blocked', 'create_date')
    search_fields = ('serial_no', 'part_no', 'model')
    list_filter = ('screen_size', 'color')


admin.site.register(Product, ProductAdmin)
