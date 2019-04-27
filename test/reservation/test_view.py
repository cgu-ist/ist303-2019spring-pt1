import pytest
from administration.models import Customer, Service
from reservation.views import validate_checked_in
from django.core.exceptions import ValidationError
from datetime import datetime
from pytz import UTC


@pytest.mark.django_db
def test_validate_checked_in_error():
    c_failed = Customer.objects.create(first_name="Karen", last_name="Snow", gender='Female',
                                       email='karen.snow@cgu.edu', tel='(661)203-7322')
    with pytest.raises(ValidationError):
        validate_checked_in(c_failed)


@pytest.mark.django_db
def test_validate_checked_in():
    c_success = Customer.objects.create(first_name="Karen", last_name="Snow", gender='Female',
                                        email='karen.snow@cgu.edu', tel='(661)203-7322',
                                        check_in_time=UTC.localize(datetime.now()))
    validate_checked_in(c_success)

