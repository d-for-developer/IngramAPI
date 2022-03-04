from import_export.resources import ModelResource
from .models import PostSaleModel


class PostSaleResources(ModelResource):
    class Meta:
        model = PostSaleModel
        import_id_fields = ("customer_email",)
        exclude = ('id', 'create_date', 'update_date',)
