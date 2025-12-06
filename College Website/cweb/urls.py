"""
URL configuration for cweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cwebapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-tables/', views.admin_tables, name='admin_tables'),
    path('admin-forms/', views.admin_forms, name='admin_forms'),
    path('admin-charts/', views.admin_charts, name='admin_charts'),
    path('admin-profile/', views.admin_profile, name='admin_profile'),
    path('admin-settings/', views.admin_settings, name='admin_settings'),
    
    # Department Management
    path('admin-departments/', views.admin_departments_list, name='admin_departments_list'),
    path('admin-departments/add/', views.admin_department_add, name='admin_department_add'),
    path('admin-departments/<int:pk>/edit/', views.admin_department_edit, name='admin_department_edit'),
    path('admin-departments/<int:pk>/delete/', views.admin_department_delete, name='admin_department_delete'),
    
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('departments/', views.departments, name='departments'),
    path('courses/', views.courses, name='courses'),
    path('faculty/', views.faculty, name='faculty'),
    path('admissions/', views.admissions, name='admissions'),
    path('placements/', views.placements, name='placements'),
    path('events/', views.events, name='events'),
    path('contact/', views.contact, name='contact'),
    path('apply/', views.apply, name='apply'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
