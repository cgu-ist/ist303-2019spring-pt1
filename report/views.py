from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from reservation.models import Reservation
from administration.models import Customer
from reservation.views import dumpJson
from datetime import datetime
from decimal import *
from django.db.models import Q
# Create your views here.


@login_required
def billing(request):
    return render(request, 'billing/main.html', None)


@login_required
def billing_summary(request):
    data = dict()

    try:
        if request.method == 'POST':
            start = request.POST['start']
            end = request.POST['end']
            customer = Customer.objects.get(id=int(request.POST['customer_id']))
            unpaid_reservations = Reservation.objects.order_by('date').filter(customer=customer).filter(
                date__gte=start).filter(date__lte=end).filter(status__exact='N')
            cancelled_reservations = Reservation.objects.order_by('date').filter(customer=customer).filter(
                date__gte=start).filter(date__lte=end).filter(status__exact='C')
            total = 0
            for reservation in unpaid_reservations:
                period = datetime.combine(reservation.date, reservation.end_time) - datetime.combine(reservation.date, reservation.start_time)
                total += Decimal(period.total_seconds() / 60) * reservation.reservation_service.rate
            data["customer_id"] = customer.id
            data["customer_name"] = customer.full_name()
            data["start"] = start
            data["end"] = end
            data["total"] = total
            data['reservations'] = [dumpJson(r) for r in unpaid_reservations]
            data['cancelled_reservations'] = [dumpJson(r) for r in cancelled_reservations]
        data['ret'] = 0
    except ValidationError as e:
        data['ret'] = 1
        data['message'] = str(e)
    return JsonResponse(data)


@login_required
def allocation(request):
    return render(request, 'allocation/main.html', None)


@login_required
def allocation_summary(request):
    data = dict()

    try:
        if request.method == 'POST':
            customer = Customer.objects.get(id=int(request.POST['customer_id']))
            tomorrow = datetime.datetime.today().date() + datetime.timedelta(days=1)
            end_date = datetime.datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date()

            occupied = Reservation.objects.order_by('reservation_service', 'date', 'start_time')\
                .filter(date__gte=tomorrow).filter(date__lte=end_date)\
                .filter(Q(customer_id__exact=customer.id, reservation_service__name__exact='Mineral baths')
                        | ~Q(reservation_service__name__exact='Mineral baths'))

            occupied_dict = {}
            for r in occupied:
                service_name = r.reservation_service.name
                if service_name in occupied_dict:
                    occupied_dict[service_name].append(r)
                else:
                    occupied_dict[service_name] = [r]

            data = {k: occupied_dict(k) for k in occupied_dict}
        data['ret'] = 0
    except ValidationError as e:
        data['ret'] = 1
        data['message'] = str(e)
    return JsonResponse(data)


@login_required
def cal_allocation(start, end, occupied_list):
    allocation_list = []
    d = start
    c = 0
    while d <= end:
        start_of_day = d + datetime.timedelta(hours=8)
        end_of_day = d + datetime.timedelta(hours=20)
        if len(occupied_list) <= c or start < occupied_list[c].date:
            allocation_list.append((start_of_day, end_of_day))
        else:
            current_time = start_of_day
            while current_time < end_of_day:
                if len(occupied_list) == c and current_time < end_of_day:
                    allocation_list.append((current_time, end_of_day))
                    current_time = end_of_day
                else:
                    if len(occupied_list) <= c and current_time < occupied_list[c].start_time:
                        allocation_list.append((current_time, occupied_list[c].start_time))
                    current_time = occupied_list[c].end_time
                    c += 1
        d = d + datetime.timedelta(days=1)
    return allocation_list
