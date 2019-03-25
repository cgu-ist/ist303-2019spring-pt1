from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from reservation.models import Reservation
from administration.models import Customer
from administration.models import Service
import datetime


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
            valid_reservations = Reservation.objects.filter(date__gte=current_time().date())
            data['reservations'] = [dumpJson(r) for r in valid_reservations]
        else:
            customer = Customer.objects.filter(id == request.POST['customer_id'])
            reservation_service = Service.objects.filter(id == request.POST['service_id'])
            reservation_length = request.POST['reservation_length']
            reservation_date_time = datetime.datetime.strptime(request.POST['reservation_time'], '%Y-%m-%d %H:%M')
            reservation_obj = Reservation(customer=customer,
                                          reservation_date_time=reservation_date_time,
                                          reservation_length=reservation_length,
                                          reservation_service=reservation_service)
            reservation_obj.save()

            data['service'] = dumpJson(reservation_obj)
        data['ret'] = 0
    except ValidationError as e:
        data['ret'] = 1
        data['message'] = str(e)
    return JsonResponse(data)


@login_required
def new_reservation(request):
    data = dict()
    try:
        if request.method == 'POST':
            customer = Customer.objects.get(id=request.POST['customer_id'])
            reservation_service = Service.objects.get(id=request.POST['service_id'])
            reservation_length = int(request.POST['reservation_length'])
            start_datetime = datetime.datetime.strptime(request.POST['reservation_date'] + ' '
                                                        + request.POST['reservation_time']
                                                        , '%Y-%m-%d %H:%M')
            end_datetime = start_datetime + datetime.timedelta(minutes=reservation_length)

            date = start_datetime.date()
            start_time = start_datetime.time()
            end_time = end_datetime.time()
            reservation_obj = Reservation(customer=customer,
                                          date=date,
                                          start_time=start_time,
                                          end_time=end_time,
                                          reservation_service=reservation_service)
            reservation_obj.full_clean()
            validate_self(reservation_obj)
            validate_other(reservation_obj)
            reservation_obj.save()
        data['ret'] = 0
    except ValidationError as e:
        data['ret'] = 1
        data['message'] = str(e)
    return JsonResponse(data)


@login_required
def delete_reservation(request):
    data = dict()
    try:
        if request.method == 'POST':
            reservation_obj = Reservation.objects.get(id=request.POST['id'])
            validateDelete(reservation_obj)
            reservation_obj.delete()
        data['ret'] = 0
    except ValidationError as e:
        data['ret'] = 1
        data['message'] = str(e)
    return JsonResponse(data)


def dumpJson(reservation_obj):
    print(reservation_obj)
    customer = reservation_obj.customer
    service = reservation_obj.reservation_service
    date = reservation_obj.date
    start_time = reservation_obj.start_time
    end_time = reservation_obj.end_time

    start_datetime = datetime.datetime.combine(date, start_time) + datetime.timedelta(hours=7)
    end_datetime = datetime.datetime.combine(date, end_time) + datetime.timedelta(hours=7)
    period = int((end_datetime - start_datetime).total_seconds() / 60)
    amount = period * service.rate

    return {
            'id': reservation_obj.id,
            'customer': {
                'id': customer.id,
                'first_name': customer.first_name,
                'last_name': customer.last_name
            },
            'datetime_start_ms': start_datetime.strftime('%s') + '000',
            'datetime_end_ms': end_datetime.strftime('%s') + '000',
            'date' : reservation_obj.date,
            'start_time': reservation_obj.start_time,
            'period': period,
            'amount': amount,
            'reservation_service': {
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'time_type': service.time_type,
                'rate': service.rate
            }
    }


def validateDelete(reservation):
    reservation_datetime = datetime.datetime.combine(reservation.date, reservation.start_time)
    if reservation_datetime < current_time():
        raise ValidationError(f"You are not supposed to cancel a stated reservation.")
    if reservation_datetime - current_time() <= datetime.timedelta(minutes=10):
        raise ValidationError(f"You can't cancel the reservation now service will be started within 10 minutes.")


def validate_self(validating):
    left = Reservation.objects.filter(customer=validating.customer).filter(date=validating.date).filter(
        start_time__lte=validating.start_time).filter(end_time__gt=validating.start_time)
    right = Reservation.objects.filter(customer=validating.customer).filter(date=validating.date).filter(
        start_time__lt=validating.end_time).filter(end_time__gte=validating.start_time)

    if left.count() + right.count() > 0:
        raise ValidationError(f"Multiple reservation at the same time is not allowed.")


def validate_other(validating):
    limit = validating.reservation_service.limit

    check_date_time = datetime.datetime.combine(validating.date, validating.start_time)
    check_end_time = datetime.datetime.combine(validating.date, validating.end_time)

    while check_date_time < check_end_time:
        check_time = check_date_time.time()
        overlap = Reservation.objects.filter(reservation_service=validating.reservation_service).filter(
            date=validating.date).filter(start_time__lte=check_time).filter(end_time__gt=check_time)
        if overlap.count() >= limit:
            raise ValidationError(f"Reservation numbers at the {check_time} is beyond limit {limit}.")
        check_date_time += datetime.timedelta(minutes=30)


def current_time():
    return datetime.datetime.now() + datetime.timedelta(hours=-7)



