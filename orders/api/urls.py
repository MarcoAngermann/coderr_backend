from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.OrdersListAPIView.as_view()),
    path('orders/<int:pk>/', views.SingleOrderAPIView.as_view()),  # Ändere `id` zu `pk`
    path('order-count/<int:pk>/', views.OrdersBusinessUncompletedCountAPIView.as_view()),  # Ändere `id` zu `pk`
    path('completed-order-count/<int:pk>/', views.OrdersBusinessCompletedCountAPIView.as_view()),  # Ändere `id` zu `pk`
]

