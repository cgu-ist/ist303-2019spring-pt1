import pytest


@pytest.mark.django_db
def test_service_list(admin_client):
    response = admin_client.get('/service/list')
    assert response.status_code == 200
