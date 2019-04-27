import pytest
from administration.models import Customer, Service


@pytest.mark.django_db
def test_service_create(admin_client):
    c1 = Customer.objects.create(first_name="Karen", last_name="Snow", gender='Female', email='karen.snow@cgu.edu',
                                 tel='(661)203-7322')
    s1 = Service.objects.create(name='Mineral baths', description='Mineral baths', min_service_time=15,
                                max_service_time=60, rate=2.50, limit=65535)

    data = {
        'customer_id': c1.id,
        'service_id': s1.id,
        'reservation_length': 90,
        'reservation_date': '2019-03-30',
        'reservation_time': '16:30'
    }
    response = admin_client.post('/reservation/new', data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_service_create(admin_client):
    c1 = Customer.objects.create(first_name="Karen", last_name="Snow", gender='Female', email='karen.snow@cgu.edu',
                                 tel='(661)203-7322')
    s1 = Service.objects.create(name='Mineral baths', description='Mineral baths', min_service_time=15,
                                max_service_time=60, rate=2.50, limit=65535)


    data = {
        'customer_id': c1.id,
        'service_id': s1.id,
        'reservation_length': 90,
        'reservation_date': '2019-03-30',
        'reservation_time': '16:30'
    }
    response = admin_client.post('/reservation/new', data)
    assert response.status_code == 200
