from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import (Service, Customer)
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from datetime import datetime
import random


# Create your views here.
@login_required
def service_base(request):
    return render(request, 'service/main.html', None)


@login_required
def service_list(request):
    data = dict()
    try:
        if request.method == 'GET':
            servicelist = [service2json(x) for x in Service.objects.all()]
            data['services'] = servicelist
        else:
            if request.POST['limit'] == "":
                service = Service(name=request.POST['name'],
                                  description=request.POST['description'],
                                  min_service_time=request.POST['min_service_time'],
                                  max_service_time=request.POST['max_service_time'],
                                  rate=request.POST['rate'])
            else:
                service = Service(name=request.POST['name'],
                                  description=request.POST['description'],
                                  min_service_time=request.POST['min_service_time'],
                                  max_service_time=request.POST['max_service_time'],
                                  rate=request.POST['rate'],
                                  limit=request.POST['limit'])
            service.full_clean()
            service.save()

            data['service'] = service2json(service)
        data['ret'] = 0
    except ValidationError as e:
        data['ret'] = 1
        data['message'] = str(e)
    return JsonResponse(data)


def service2json(service):
    if service.limit == 65535:
        limit = "Unlimited"
    else:
        limit = service.limit

    return {
            'id': service.id,
            'name': service.name,
            'description': service.description,
            'min_service_time': service.min_service_time,
            'max_service_time': service.max_service_time,
            'rate': service.rate,
            'limit': limit
    }


@login_required
def service_detail(request, service_id):
    data = dict()
    try:
        service = Service.objects.get(id=service_id)

        if request.method == 'POST':
            if request.POST['name'] is not None:
                service.name = request.POST['name']
            if request.POST['description'] is not None:
                service.description = request.POST['description']
            if request.POST['min_service_time'] is not None:
                service.min_service_time = request.POST['min_service_time']
            if request.POST['max_service_time'] is not None:
                service.max_service_time = request.POST['max_service_time']
            if request.POST['rate'] is not None:
                service.rate = request.POST['rate']
            if request.POST['limit'] is None or request.POST['limit'] == "":
                service.limit = 65535
            else:
                service.limit = request.POST['limit']
            service.full_clean()
            service.save()
        elif request.method == 'DELETE':
            service.delete()

        if service.limit == 65535:
            limit = "Unlimited"
        else:
            limit = service.limit
        data['ret'] = 0
        data['service'] = service2json(service)
        return JsonResponse(data)
    except ValidationError as e:
        data['ret'] = 1
        data['message'] = str(e)
    return JsonResponse(data)


@login_required
def customer_base(request):
    return render(request, 'customer/main.html', None)


@login_required
def customer_list(request):
    data = dict()
    try:
        if request.method == 'GET':
            customers = list(Customer.actives.all().values())
            data['customers'] = customers
        else:
            customer = Customer(first_name=request.POST['first_name'],
                              last_name=request.POST['last_name'],
                              gender=request.POST['gender'],
                              email=request.POST['email'],
                              tel=request.POST['tel'])
            customer.full_clean()
            customer.save()

            data['customer'] = {
                    'id': customer.id,
                    'first_name': customer.first_name,
                    'last_name': customer.last_name,
                    'gender': customer.gender,
                    'email': customer.email,
                    'tel': customer.tel
                }
        data['ret'] = 0
    except ValidationError as e:
        data['ret'] = 1
        data['message'] = str(e)
    return JsonResponse(data)


@login_required
def customer_detail(request, customer_id):
    data = dict()
    try:
        customer = Customer.actives.get(id=customer_id)

        if request.method == 'POST':
            if request.POST['first_name'] is not None:
                customer.first_name = request.POST['first_name']
            if request.POST['last_name'] is not None:
                customer.last_name = request.POST['last_name']
            if request.POST['gender'] is not None:
                customer.gender = request.POST['gender']
            if request.POST['email'] is not None:
                customer.email = request.POST['email']
            if request.POST['tel'] is not None:
                customer.tel = request.POST['tel']
            customer.full_clean()
            customer.save()
        elif request.method == 'DELETE':
            customer.delete()

        data['ret'] = 0
        data['customer'] = {
                'id': customer.id,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'gender': customer.gender,
                'email': customer.email,
                'tel': customer.tel
            }
        return JsonResponse(data)
    except ValidationError as e:
        data['ret'] = 1
        data['message'] = str(e)
    return JsonResponse(data)


@login_required
def customer_check_in(request, customer_id):
    data = dict()
    try:
        customer = Customer.actives.get(id=customer_id)

        customer.check_in_time = datetime.now()
        customer.full_clean()
        customer.save()

        data['ret'] = 0
        data['customer'] = {
                'id': customer.id,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'gender': customer.gender,
                'email': customer.email,
                'tel': customer.tel,
                'check_in_number': random.randint(1000000, 9999999)
            }
        return JsonResponse(data)
    except ValidationError as e:
        data['ret'] = 1
        data['message'] = str(e)
    return JsonResponse(data)
