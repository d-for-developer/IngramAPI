from django.urls import path
from . import views

app_name = 'postsale'

urlpatterns = [
    # ex: api/postsale/<str:token>/
    path('<str:token>/', views.PostSaleListView.as_view(), name='all'),
    # ex: api/postsale/<str:token>/create/
    path('create/<str:token>/', views.PostSaleCreateView.as_view(), name='postsale_create'),
]