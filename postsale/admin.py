from django.contrib import admin
from .models import PostSaleModel
from import_export.admin import ImportExportModelAdmin
from .resources import PostSaleResources


# Register your models here.

class PostSaleAdmin(ImportExportModelAdmin):
    resource_class = PostSaleResources
    search_fields = ('assetMake', 'customer_name', 'customer_email')
    list_display = ('assetMake', 'customer_name', 'customer_email', 'OA_Plan_name', 'start_date', 'end_date')
    list_filter = ('assetMake', 'customer_name', 'customer_email', 'OA_Plan_name', 'start_date', 'end_date')


admin.site.register(PostSaleModel, PostSaleAdmin)