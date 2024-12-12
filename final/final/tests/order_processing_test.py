import pytest
from django.test import Client

@pytest.mark.django_db
def test_order_processing():
    client = Client()
    response = client.post('/api/orders/', {'product_id': 1, 'quantity': 2})
    assert response.status_code == 201
    assert 'order_id' in response.json()