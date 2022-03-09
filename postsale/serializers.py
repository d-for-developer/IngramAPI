from requests import Response
from rest_framework.serializers import ModelSerializer

from .models import PostSaleModel


class PostSaleSerializer(ModelSerializer):
    """
    PostSaleSerializer is a model serializer which shows the attributes
    of a user.
    """

    class Meta:
        model = PostSaleModel
        fields = ('customer_name',
                  'customer_email',
                  'customer_mobile_no',
                  'product_name',
                  'assetMake',
                  'assetModel',
                  'serialNo',
                  'invoiceDate',
                  'invoiceValue',
                  'customer_address',
                  'pin_code',
                  'city',
                  'state',
                  'OA_Plan_name',
                  'OA_plan_price_paid_by_seller',
                  'OA_plan_price_to_customer',
                  'partner_name',
                  'partner_bu_name',
                  'MembershipId',
                  'primary_customerID',
                  'start_date',
                  'end_date')


