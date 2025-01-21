from django.urls import path
from .views import OrderList, OrderDetail

urlpatterns = [
    path('orders/', OrderList.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetail.as_view(), name='order-detail'),
]
