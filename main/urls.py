from django.urls import path
from main.views import *

urlpatterns = [
    path('seller/create/', SellerCreateApiView.as_view(), name='seller-create'),
    path('seller/retrieve/<int:pk>/', SellerRetrieveApiView.as_view(), name='seller-retrieve'),
    path('seller/update/<int:pk>/', SellerUpdateApiView.as_view(), name='seller-update'),
    path('seller/delete/<int:pk>/', SellerDestroyApiView.as_view(), name='seller-delete'),
    path('seller/list/', SellerListApiView.as_view(), name='seller-list'),
]
