from django.urls import path
from website_template_app import views

urlpatterns = [
    path('',views.home,name='home'),
    path('index',views.home,name='home'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('menu',views.menu,name='menu'),
    path('news-detail',views.newsdetail,name='newsdetail'),
    path('news',views.news,name='news')
]