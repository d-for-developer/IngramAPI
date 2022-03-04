from django.urls import path

from . import views


app_name = 'product'

urlpatterns = [
    # ex: api/product/<str:token>/
    path('<str:token>/', views.ListProductView.as_view(), name='List Product'),
    # ex: api/product/<str:token>/validate/
    path('<str:token>/validate/', views.ValidateSerialNoView.as_view(), name='Validate Product'),
    # ex: api/product/<str:token>/block/
    path('<str:token>/block/', views.BlockProductView.as_view(), name='Block Product'),
]
