from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from reservation.models import Reservation
from administration.models import Customer
from administration.models import Service

# Create your views here.
@login_required
def reservation(request):
    return render(request, 'reservation.html', None)


class DayHtml(TemplateView):
    template_name = "calendar/day.html"


class DayHtml(TemplateView):
    template_name = "calendar/day.html"


class EventsListHtml(TemplateView):
    template_name = "calendar/events-list.html"


class ModalHtml(TemplateView):
    template_name = "calendar/modal.html"


class MonthHtml(TemplateView):
    template_name = "calendar/month.html"


class MonthDayHtml(TemplateView):
    template_name = "calendar/month-day.html"


class WeekHtml(TemplateView):
    template_name = "calendar/week.html"


class WeekDaysHtml(TemplateView):
    template_name = "calendar/week-days.html"


class YearHtml(TemplateView):
    template_name = "calendar/year.html"


class YearMonthHtml(TemplateView):
    template_name = "calendar/year-month.html"


@login_required
def reservations(request):
    data = dict()
    try:
        if request.method == 'GET':
            valid_reservations = list(Reservation.objects.values())
            data['reservations'] = valid_reservations
        else:
            customer = Customer.objects.filter(id == request.POST['customer_id'])
            reservation_service = Service.objects.filter(id == request.POST['service_id'])
            reservation_date_time = request.POST['reservation_time']
            reservation = Reservation(customer=customer, reservation_date_time=reservation_date_time,
                                  reservation_service=reservation_service)
            reservation.save()

            data['service'] = {
                    'customer': customer,
                    'reservation_date_time': reservation_date_time,
                    'reservation_service': reservation_service
                }
        data['ret'] = 0
    except ValidationError as e:
        data['ret'] = 1
        data['message'] = str(e)
    return JsonResponse(data)


@login_required
def new_reservation(request):
    return render(request, 'new_reservation.html', None)