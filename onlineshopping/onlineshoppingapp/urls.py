from django.urls import path
from onlineshoppingapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('register', views.register, name='register'),
    path('list', views.productlist, name='list'),
     path('category/<int:id>/', views.category_detail, name='category_detail'),
]