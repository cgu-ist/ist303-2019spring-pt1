import pytest
from datetime import datetime
from report.views import allocation_array
from reservation.models import Reservation
from administration.models import Customer, Service


def test_allocation_array_1():
    start = datetime(2019, 4, 30).date()
    end = datetime(2019, 5, 6).date()
    result = allocation_array(start, end, [])
    assert len(result) == 7
    assert result[0] == [1 for x in range(0, 48)]
    assert result[1] == [1 for x in range(0, 48)]
    assert result[2] == [1 for x in range(0, 48)]
    assert result[3] == [1 for x in range(0, 48)]
    assert result[4] == [1 for x in range(0, 48)]
    assert result[5] == [1 for x in range(0, 48)]
    assert result[6] == [1 for x in range(0, 48)]


def test_allocation_array_2():
    start = datetime(2019, 4, 30).date()
    end = datetime(2019, 5, 6).date()
    c = Customer(first_name="Karen", last_name="Snow", gender='Female',
                                       email='karen.snow@cgu.edu', tel='(661)203-7322')
    s = Service(name='Mineral baths', description='Mineral baths', min_service_time=15,
                                     max_service_time=60, rate=2.50, limit=65535)
    t1_s = datetime(2019, 5, 1, 12, 0)
    t1_e = datetime(2019, 5, 1, 13, 0)
    t2_s = datetime(2019, 5, 3, 10, 0)
    t2_e = datetime(2019, 5, 3, 11, 30)

    r1 = Reservation(customer=c, date=t1_s.date(), start_time=t1_s.time(), end_time=t1_e.time())
    r2 = Reservation(customer=c, date=t2_s.date(), start_time=t2_s.time(), end_time=t2_e.time())
    result = allocation_array(start, end, [r1, r2])
    assert len(result) == 7
    assert result[0] == [1 for x in range(0, 48)]
    l1 = [1 for x in range(0, 48)]
    l1[16:20] = [0, 0, 0, 0]
    assert result[1] == l1
    assert result[2] == [1 for x in range(0, 48)]
    l2 = [1 for x in range(0, 48)]
    l2[8:14] = [0, 0, 0, 0, 0, 0]
    assert result[3] == l2
    assert result[4] == [1 for x in range(0, 48)]
    assert result[5] == [1 for x in range(0, 48)]
    assert result[6] == [1 for x in range(0, 48)]
