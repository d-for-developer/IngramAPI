from rest_framework import serializers


class SerialValidationSerializer(serializers.Serializer):
    part_no = serializers.CharField(required=True,)
    serial_no = serializers.CharField(required=True,)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Product

        model = Product
        fields = ("id", "serial_no", "part_no", "title", "model", "screen_size",
                  "color", "is_emi", "is_blocked")
