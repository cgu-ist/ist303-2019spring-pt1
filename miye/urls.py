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
from django.views.generic import TemplateView

from administration import views as administration_views
from reservation import views as reservation_views
from accounts import views as accounts_views
from report import views as report_views
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
    path('reservations', reservation_views.reservations, name='reservations_main'),
    path('reservation/new', reservation_views.new_reservation, name='new_reservation'),
    path('reservation/delete', reservation_views.cancel_reservation, name='delete_reservation'),
    path('reservation', reservation_views.reservation, name='reservation_main'),
    path('reservation/calendar/day.html', reservation_views.DayHtml.as_view()),
    path('reservation/calendar/events-list.html', reservation_views.EventsListHtml.as_view()),
    path('reservation/calendar/modal.html', reservation_views.ModalHtml.as_view()),
    path('reservation/calendar/month.html', reservation_views.MonthHtml.as_view()),
    path('reservation/calendar/month-day.html', reservation_views.MonthDayHtml.as_view()),
    path('reservation/calendar/week.html', reservation_views.WeekHtml.as_view()),
    path('reservation/calendar/week-days.html', reservation_views.WeekDaysHtml.as_view()),
    path('reservation/calendar/year.html', reservation_views.YearHtml.as_view()),
    path('reservation/calendar/year-month.html', reservation_views.YearMonthHtml.as_view()),
    path('billing', report_views.billing, name='billing_main'),
    path('billing/summary', report_views.billing_summary, name='billing_summary'),
    path('home', TemplateView.as_view(template_name='home.html'))
]


urlpatterns += staticfiles_urlpatterns()
