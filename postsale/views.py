from rest_framework.generics import ListAPIView, CreateAPIView
from api_token.permissions import HasValidApiToken
from .models import PostSaleModel
from .serializers import PostSaleSerializer


class PostSaleListView(ListAPIView):
    """This endpoint allows for view of a post sale data"""
    serializer_class = PostSaleSerializer
    queryset = PostSaleModel.objects.all()
    permission_classes = (HasValidApiToken,)


class PostSaleCreateView(CreateAPIView):
    """This endpoint allows for create of a post sale data"""
    serializer_class = PostSaleSerializer

    def post(self, request, *args, **kwargs):
        if (customer_name := request.data.get("customer_name")) and (
                start_date := request.data.get("start_date")
        ):
            request.data["customer_name"] = customer_name
            request.data["start_date"] = start_date
            return self.create(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)
    permission_classes = (HasValidApiToken,)