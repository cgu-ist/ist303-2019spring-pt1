"""miye URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
from administration import views as administration_views
from accounts import views as accounts_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', accounts_views.user_login, name="login"),
    re_path(r'^login[/]?', accounts_views.user_login, name="login"),
    path('accounts/login/', accounts_views.user_login, name="login"),
    re_path('^logout[/]?', accounts_views.user_logout, name="logout"),
    re_path('^admin[/]?', admin.site.urls),
    path('service', administration_views.service_base, name='service_main'),
    path('service/list', administration_views.service_list, name="service_list"),
    path('service/<int:service_id>', administration_views.service_detail, name="service_detail"),
    path('customer', administration_views.customer_base, name='customer_main'),
    path('customer/list', administration_views.customer_list, name="customer_list"),
    path('customer/<int:customer_id>', administration_views.customer_detail, name="customer_detail"),
]


urlpatterns += staticfiles_urlpatterns()
