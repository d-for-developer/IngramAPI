from import_export.resources import ModelResource
from .models import Product


class ProductResources(ModelResource):
    class Meta:
        model = Product
        import_id_fields = ("serial_no",)
        exclude = ('id', 'create_date', 'update_date',)
