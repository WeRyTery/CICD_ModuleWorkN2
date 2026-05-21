from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('category/<str:name>/', views.category_detail, name='category_detail'),
]
