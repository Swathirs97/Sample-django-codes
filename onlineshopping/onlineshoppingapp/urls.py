from django.urls import path
from onlineshoppingapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('register', views.register, name='register'),
    path('list', views.productlist, name='list'),
    path('category/<int:id>/', views.category_detail, name='category_detail'),
    path('edit/<int:p_id>/', views.edit_product, name='edit'),
    path('delete/<int:p_id>/', views.delete_product, name='delete'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('search',views.search,name='search')
]