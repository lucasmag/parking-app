import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
from decimal import Decimal

User = get_user_model()

@pytest.fixture(scope='session')
def django_db_setup():
    """Database setup for tests"""
    pass

@pytest.fixture
def api_client():
    """Provide API client for tests"""
    return APIClient()

@pytest.fixture
def authenticated_client(api_client):
    """Provide authenticated API client using Factory Boy"""
    from src.tests.factories import UserFactory
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    api_client.user = user
    return api_client
