import pytest
from django.core.exceptions import ValidationError
from administration.models import Service, Customer


@pytest.mark.django_db
def test_customer_create():
    haibo = Customer.objects.create(first_name="Haibo", last_name="Yan", gender='Male', email='haibo.yan@cgu.edu',
                                    tel='(925)351-5817')
    assert haibo is not None


@pytest.mark.django_db
def test_customer_bulk_create():
    customers = Customer.objects.bulk_create([
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
    assert len(customers) == 5


@pytest.mark.django_db
def test_service_create():
    service = Service.objects.create(name='Mineral baths', description='Mineral baths', min_service_time=15,
                                     max_service_time=60, rate=2.50, limit=65535)
    assert service is not None
    service.delete()


@pytest.mark.django_db
def test_service_create_with_invalid_service_time():
    with pytest.raises(ValidationError) as e:
        service = Service(name='Mineral baths', description='Mineral baths', min_service_time=5,
                               max_service_time=60, rate=2.50, limit=65535)
        service.full_clean()
    errorMsag = e.value.args[0]['min_service_time'][0].messages[0]
    assert errorMsag == '5 is not a multiplication of 15.'


