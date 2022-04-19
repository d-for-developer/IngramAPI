from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView

from api_token.permissions import HasValidApiToken


class ListProductView(ListAPIView):
    from .models import Product
    from .serializers import ProductSerializer

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (HasValidApiToken,)


class ProductDetailView(ListAPIView):
    from .serializers import ProductSerializer

    def get_queryset(self):
        from .models import Product
        sno = self.request.GET['serial_no']
        queryset = Product.objects.filter(serial_no=sno)
        return queryset

    serializer_class = ProductSerializer
    permission_classes = (HasValidApiToken,)


class ValidateSerialNoView(GenericAPIView):
    """
    Handles the post request and checks if the serial number provided is valid
    """
    from .serializers import SerialValidationSerializer

    serializer_class = SerialValidationSerializer
    permission_classes = (HasValidApiToken,)

    def post(self, request, *args, **kwargs):
        from drfaddons.utils import CustomJsonResponse
        from .models import Product
        from .serializers import SerialValidationSerializer

        serializer = SerialValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Response Data
        data = dict()

        try:
            product = Product.objects.get(part_no=serializer.validated_data['part_no'],
                                          serial_no=serializer.validated_data['serial_no'])
            if not product.is_emi:
                data['code'] = 1
                data['description'] = "Device is not available for EMI."
            elif product.is_emi and product.is_blocked:
                data['code'] = 3
                data['description'] = "The device has already been sold/activated."
            elif product.is_emi and not product.is_blocked:
                data['code'] = 0
                data['description'] = "Device is available for EMI."

            return CustomJsonResponse(data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            data['code'] = 2
            data['detail'] = "The serial number does not exist or model mismatch."
            return CustomJsonResponse(data, status=status.HTTP_404_NOT_FOUND)


class BlockProductView(GenericAPIView):
    """
    Handles the post request and Block the product if available for emi
    """
    from .serializers import SerialValidationSerializer

    serializer_class = SerialValidationSerializer
    permission_classes = (HasValidApiToken,)

    def post(self, request, *args, **kwargs):
        from drfaddons.utils import CustomJsonResponse
        from .models import Product
        from .serializers import SerialValidationSerializer

        serializer = SerialValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Response Data
        data = dict()

        try:
            product = Product.objects.get(part_no=serializer.validated_data['part_no'],
                                          serial_no=serializer.validated_data['serial_no'])

            if not product.is_emi:
                data['code'] = 1
                data['description'] = "Device is not available for EMI."
            elif product.is_emi and product.is_blocked:
                data['code'] = 3
                data['description'] = "The device has already been sold/activated."
            elif product.is_emi and not product.is_blocked:
                product.is_blocked = True
                product.save()
                data['code'] = 4
                data['description'] = "Success, device is now blocked."

            return CustomJsonResponse(data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            data['code'] = 2
            data['detail'] = "The serial number does not exist or model mismatch."
            return CustomJsonResponse(data, status=status.HTTP_404_NOT_FOUND)


class UnblockProductView(GenericAPIView):
    """
    Handles the post request and Block the product if available for emi
    """
    from .serializers import SerialValidationSerializer

    serializer_class = SerialValidationSerializer
    permission_classes = (HasValidApiToken,)

    def post(self, request, *args, **kwargs):
        from drfaddons.utils import CustomJsonResponse
        from .models import Product
        from .serializers import SerialValidationSerializer

        serializer = SerialValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Response Data
        data = dict()

        try:
            product = Product.objects.get(part_no=serializer.validated_data['part_no'],
                                          serial_no=serializer.validated_data['serial_no'])

            if not product.is_emi:
                data['code'] = 1
                data['description'] = "Device is not available for EMI."
            elif product.is_emi and product.is_blocked:
                product.is_blocked = False
                product.save()
                data['code'] = 4
                data['description'] = "Success, device is now unblocked."
            elif product.is_emi and not product.is_blocked:
                data['code'] = 3
                data['description'] = "Device is now available for EMI."
            return CustomJsonResponse(data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            data['code'] = 2
            data['detail'] = "The serial number does not exist or model mismatch."
            return CustomJsonResponse(data, status=status.HTTP_404_NOT_FOUND)
