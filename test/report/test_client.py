import pytest
from administration.models import (Customer, Service)
from reservation.models import Reservation
from datetime import (date, time)
import json


@pytest.fixture(autouse=True)
def django_db_setup(django_db_createdb, db):
    Customer.objects.bulk_create([
        Customer(first_name="Haibo", last_name="Yan", gender='Male', email='haibo.yan@cgu.edu', tel='(925)351-5817'),
        Customer(first_name="Karen", last_name="Snow", gender='Female', email='karen.snow@cgu.edu',
                 tel='(661)203-7322'),
        Customer(first_name="Okechukwu", last_name="Ugwuanyi", gender='Male', email='okechukwu.ugwuanyi@cgu.edu',
                 tel='(333)828-3880'),
        Customer(first_name="Leslie", last_name="Bienenfeld", gender='Female', email='leslie.bienenfeld@cgu.edu',
                 tel='(221)323-8320'),
        Customer(first_name="Lade", last_name="Johnson", gender='Female', email='lade.johnson@cgu.edu',
                 tel='(556)741-2231'),
        Customer(first_name="Stephen", last_name="Davison", gender='Male', email='stephen.davison@cgu.edu',
                 tel='(441)323-8320')
    ])

    Service.objects.bulk_create([
        Service(name='Mineral baths', description='Mineral baths', min_service_time=15, max_service_time=60, rate=2.50,
                limit=65535),
        Service(name='Massage services', description='Swedish, shiatsu, or deep tissue', min_service_time=15,
                max_service_time=60, rate=3.00, limit=1),
        Service(name='Facial services', description='normal or collagen', min_service_time=15, max_service_time=60,
                rate=2.00, limit=1),

        Service(name='Specialty treatment services',
                description='hot stone, sugar scrub, herbal body wrap, or botanical mud wrap', min_service_time=60,
                max_service_time=90, rate=3.50, limit=1)
    ])

    day420 = date(year=2019, month=4, day=29)
    day421 = date(year=2019, month=4, day=21)
    day422 = date(year=2019, month=4, day=22)
    day423 = date(year=2019, month=4, day=23)
    day430 = date(year=2019, month=4, day=30)
    day501 = date(year=2019, month=5, day=1)
    day502 = date(year=2019, month=5, day=2)
    day503 = date(year=2019, month=5, day=3)
    day504 = date(year=2019, month=5, day=4)
    day505 = date(year=2019, month=5, day=5)
    day506 = date(year=2019, month=5, day=6)
    day507 = date(year=2019, month=5, day=7)
    day508 = date(year=2019, month=5, day=8)
    day509 = date(year=2019, month=5, day=8)
    day510 = date(year=2019, month=5, day=10)
    day511 = date(year=2019, month=5, day=11)
    day512 = date(year=2019, month=5, day=12)
    time0800 = time(hour=8, minute=0)
    time0830 = time(hour=8, minute=30)
    time0900 = time(hour=9, minute=0)
    time0930 = time(hour=9, minute=30)
    time1000 = time(hour=10, minute=0)
    time1030 = time(hour=10, minute=30)
    time1100 = time(hour=11, minute=0)
    time1130 = time(hour=11, minute=30)
    time1200 = time(hour=12, minute=0)
    time1230 = time(hour=12, minute=30)
    time1300 = time(hour=13, minute=0)
    time1330 = time(hour=13, minute=30)
    time1400 = time(hour=14, minute=0)
    time1430 = time(hour=14, minute=30)
    time1500 = time(hour=15, minute=0)
    time1530 = time(hour=15, minute=30)
    time1600 = time(hour=16, minute=0)
    time1630 = time(hour=16, minute=30)
    time1700 = time(hour=17, minute=0)
    time1730 = time(hour=17, minute=30)
    time1800 = time(hour=18, minute=0)
    time1830 = time(hour=18, minute=30)
    time1900 = time(hour=19, minute=0)
    time1930 = time(hour=19, minute=30)
    time2000 = time(hour=20, minute=0)
    haibo = Customer.objects.get(first_name='Haibo')
    leslie = Customer.objects.get(first_name='Leslie')
    okey = Customer.objects.get(first_name='Okechukwu')
    stephen = Customer.objects.get(first_name='Stephen')
    karen = Customer.objects.get(first_name='Karen')
    lade = Customer.objects.get(first_name='Lade')
    s1 = Service.objects.get(name='Mineral baths')
    s2 = Service.objects.get(name='Massage services')
    s3 = Service.objects.get(name='Facial services')
    s4 = Service.objects.get(name='Specialty treatment services')
    Reservation.objects.bulk_create([
        Reservation(customer=okey, date=day420, start_time=time1330, end_time=time1430, reservation_service=s4,
                    status='C'),
        Reservation(customer=lade, date=day421, start_time=time0800, end_time=time0900, reservation_service=s1,
                    status='N'),
        Reservation(customer=stephen, date=day422, start_time=time1430, end_time=time1530, reservation_service=s2,
                    status='N'),
        Reservation(customer=leslie, date=day423, start_time=time1730, end_time=time1830, reservation_service=s3,
                    status='N'),
        Reservation(customer=karen, date=day430, start_time=time1900, end_time=time2000, reservation_service=s1,
                    status='N'),
        Reservation(customer=haibo, date=day501, start_time=time1400, end_time=time1500, reservation_service=s1,
                    status='N'),
        Reservation(customer=lade, date=day501, start_time=time1200, end_time=time1330, reservation_service=s1,
                    status='N'),
        Reservation(customer=okey, date=day501, start_time=time1700, end_time=time1900, reservation_service=s4,
                    status='N'),
        Reservation(customer=stephen, date=day501, start_time=time0900, end_time=time1030, reservation_service=s2,
                    status='N'),
        Reservation(customer=leslie, date=day502, start_time=time0900, end_time=time1030, reservation_service=s2,
                    status='N'),
        Reservation(customer=karen, date=day502, start_time=time1900, end_time=time2000, reservation_service=s3,
                    status='N'),
        Reservation(customer=haibo, date=day502, start_time=time1730, end_time=time1900, reservation_service=s3,
                    status='N'),
        Reservation(customer=lade, date=day502, start_time=time1030, end_time=time1200, reservation_service=s2,
                    status='N'),
        Reservation(customer=okey, date=day502, start_time=time1200, end_time=time1300, reservation_service=s4),
        Reservation(customer=stephen, date=day503, start_time=time0800, end_time=time0830, reservation_service=s1,
                    status='N'),
        Reservation(customer=leslie, date=day503, start_time=time1200, end_time=time1330, reservation_service=s1,
                    status='N'),
        Reservation(customer=karen, date=day503, start_time=time1400, end_time=time1500, reservation_service=s1,
                    status='N'),
        Reservation(customer=haibo, date=day504, start_time=time0900, end_time=time1000, reservation_service=s4,
                    status='N'),
        Reservation(customer=lade, date=day504, start_time=time1000, end_time=time1030, reservation_service=s1,
                    status='N'),
        Reservation(customer=okey, date=day504, start_time=time1030, end_time=time1100, reservation_service=s1,
                    status='N'),
        Reservation(customer=stephen, date=day504, start_time=time1500, end_time=time1530, reservation_service=s1,
                    status='N'),
        Reservation(customer=leslie, date=day504, start_time=time1900, end_time=time2000, reservation_service=s1,
                    status='N'),
        Reservation(customer=karen, date=day505, start_time=time1500, end_time=time1600, reservation_service=s3,
                    status='N'),
        Reservation(customer=haibo, date=day506, start_time=time1200, end_time=time1300, reservation_service=s2,
                    status='N'),
        Reservation(customer=lade, date=day507, start_time=time1400, end_time=time1500, reservation_service=s3,
                    status='N'),
        Reservation(customer=haibo, date=day508, start_time=time0930, end_time=time1030, reservation_service=s2,
                    status='N'),
        Reservation(customer=karen, date=day509, start_time=time1100, end_time=time1130, reservation_service=s1,
                    status='N'),
        Reservation(customer=okey, date=day510, start_time=time1230, end_time=time1330, reservation_service=s3,
                    status='N'),
        Reservation(customer=okey, date=day510, start_time=time1930, end_time=time2000, reservation_service=s2,
                    status='N'),
        Reservation(customer=leslie, date=day511, start_time=time0800, end_time=time0900, reservation_service=s4,
                    status='N'),
        Reservation(customer=haibo, date=day511, start_time=time1800, end_time=time1830, reservation_service=s4,
                    status='N'),
        Reservation(customer=stephen, date=day512, start_time=time1630, end_time=time1700, reservation_service=s4,
                    status='N')
    ])


def test_billing_summary(admin_client):
    haibo = Customer.objects.get(first_name='Haibo')
    data = {
        'start': '2019-04-30',
        'end': '2019-05-06',
        'customer_id': haibo.id
    }
    response = admin_client.post('/billing/summary', data)
    assert response.status_code == 200

    billing_json = json.loads(response.getvalue())
    assert len(billing_json['reservations']) == 4
    assert len(billing_json['cancelled_reservations']) == 0
