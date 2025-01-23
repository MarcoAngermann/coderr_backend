from django.urls import path
from . import views

urlpatterns = [
  path('base-info/', views.BaseInfoViews.as_view()),
]
