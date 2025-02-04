from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.OrdersListAPIView.as_view()),
    path('orders/<int:pk>/', views.SingleOrderAPIView.as_view()), 
    path('order-count/<int:pk>/', views.OrdersBusinessUncompletedCountAPIView.as_view()), 
    path('completed-order-count/<int:pk>/', views.OrdersBusinessCompletedCountAPIView.as_view()),  
]

