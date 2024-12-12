import pytest
from django.contrib.auth.models import User
from django.test import Client

@pytest.mark.django_db
def test_user_authentication():
    client = Client()
    user = User.objects.create_user(username='testuser', password='testpassword')
    response = client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    assert 'access' in response.json()
