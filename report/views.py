from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from reservation.models import Reservation
from administration.models import Customer, Service
from reservation.views import dumpJson
from datetime import datetime, timedelta, time
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
            services = Service.objects.all()
            today = datetime.today().date()
            end_date = datetime.strptime(request.POST['end'], '%Y-%m-%d').date()

            occupied = Reservation.objects.order_by('reservation_service', 'date', 'start_time')\
                .filter(date__gte=today).filter(date__lte=end_date)\
                .filter(Q(customer_id__exact=customer.id, reservation_service__name__exact='Mineral baths')
                        | ~Q(reservation_service__name__exact='Mineral baths'))

            occupied_dict = {}
            for r in occupied:
                service_name = r.reservation_service.name
                if service_name in occupied_dict:
                    occupied_dict[service_name].append(r)
                else:
                    occupied_dict[service_name] = [r]

            allocations = {k: allocation_array(today, end_date, v) for k, v in occupied_dict.items()}

            for service in services:
                if service.name not in allocations:
                    allocations[service.name] = allocation_array(today, end_date, [])
            data['start'] = today
            data['end'] = end_date
            data['allocations'] = allocations
        data['ret'] = 0
    except ValidationError as e:
        data['ret'] = 1
        data['message'] = str(e)
    return JsonResponse(data)


def cal_allocation(start, end, occupied_list):
    allocation_list = []
    d = start
    c = 0
    while d <= end:
        start_of_day = datetime.combine(d, time(8, 0))
        end_of_day = datetime.combine(d, time(20, 0))
        if len(occupied_list) <= c or d != occupied_list[c].date:
            allocation_list.append({'start': start_of_day, 'end': end_of_day})
        else:
            current_time = start_of_day
            while current_time < end_of_day:
                if len(occupied_list) == c and current_time < end_of_day:
                    allocation_list.append({'start': current_time, 'end': end_of_day})
                    current_time = end_of_day
                else:
                    if len(occupied_list) > c and current_time < \
                            datetime.combine(occupied_list[c].date, occupied_list[c].start_time):
                        allocation_list.append({'start': current_time,
                                                'end': datetime.combine(occupied_list[c].date,
                                                                        occupied_list[c].start_time)})
                    current_time = datetime.combine(occupied_list[c].date, occupied_list[c].end_time)
                    c += 1
        d = d + timedelta(days=1)
    return allocation_list


def allocation_array(start, end, occupied_list):
    allocation_list = []
    d = start
    c = 0
    while d <= end:
        dl = []
        start_of_day = datetime.combine(d, time(8, 0))
        end_of_day = datetime.combine(d, time(20, 0))
        ct = start_of_day
        while ct < end_of_day:
            if len(occupied_list) == c or ct < datetime.combine(occupied_list[c].date, occupied_list[c].start_time):
                dl.append(1)
            else:
                dl.append(0)

            ct += timedelta(minutes=15)
            if len(occupied_list) > c and ct >= datetime.combine(occupied_list[c].date, occupied_list[c].end_time):
                c += 1
        allocation_list.append(dl)
        d += timedelta(days=1)

    return allocation_list
