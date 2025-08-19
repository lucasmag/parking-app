import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from tests.factories import UserFactory

User = get_user_model()

@pytest.mark.unit
class TestUserAuthentication:
    
    @pytest.mark.django_db
    def test_user_registration_success(self, api_client):
        """Test successful user registration"""
        user_data = {
            'email': 'newuser@test.com',
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123'
        }
        
        url = reverse('user-list')
        response = api_client.post(url, user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['user']['email'] == user_data['email']
        
        # Verify user was created in database
        user = User.objects.get(email=user_data['email'])
        assert user.username == user_data['username']
        assert user.first_name == user_data['first_name']

    @pytest.mark.django_db
    @pytest.mark.parametrize("field,value,expected_error", [
        ('email', 'invalid-email', 'Enter a valid email address'),
        ('password', '123', 'This password is too short'),
        ('password_confirm', 'different', "Passwords don't match"),
    ])
    def test_user_registration_validation(self, api_client, field, value, expected_error):
        """Test user registration validation errors"""
        user_data = {
            'email': 'test@test.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123'
        }
        user_data[field] = value
        
        url = reverse('user-list')
        response = api_client.post(url, user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        if field == 'password_confirm':
            assert expected_error in str(response.data)
        else:
            assert field in response.data

    @pytest.mark.django_db
    def test_duplicate_email_registration(self, api_client):
        """Test registration with existing email fails"""
        existing_user = UserFactory(email='existing@test.com')
        
        user_data = {
            'email': 'existing@test.com',
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123'
        }
        
        url = reverse('user-list')
        response = api_client.post(url, user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    @pytest.mark.django_db
    def test_user_login_success(self, api_client):
        """Test successful user login"""
        password = 'testpass123'
        user = UserFactory(password=password)
        
        url = reverse('user-login')
        response = api_client.post(url, {
            'email': user.email,
            'password': password
        })
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['user']['email'] == user.email

    @pytest.mark.django_db
    @pytest.mark.parametrize("email,password,expected_status", [
        ('wrong@email.com', 'testpass123', status.HTTP_400_BAD_REQUEST),
        ('test@email.com', 'wrongpassword', status.HTTP_400_BAD_REQUEST),
        ('', 'testpass123', status.HTTP_400_BAD_REQUEST),
        ('test@email.com', '', status.HTTP_400_BAD_REQUEST),
    ])
    def test_user_login_invalid_credentials(self, api_client, email, password, expected_status):
        """Test login with invalid credentials"""
        UserFactory(email='test@email.com', password='testpass123')
        
        url = reverse('user-login')
        response = api_client.post(url, {'email': email, 'password': password})
        
        assert response.status_code == expected_status

    @pytest.mark.django_db
    def test_user_logout_success(self, authenticated_client):
        """Test successful user logout"""
        # Get refresh token
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(authenticated_client.user)
        
        url = reverse('user-logout')
        response = authenticated_client.post(url, {'refresh': str(refresh)})
        
        assert response.status_code == status.HTTP_205_RESET_CONTENT
        assert 'Successfully logged out' in response.data['message']

    @pytest.mark.django_db
    def test_user_profile_access(self, authenticated_client):
        """Test accessing user profile"""
        url = reverse('user-profile')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['user']['email'] == authenticated_client.user.email

    @pytest.mark.django_db
    def test_change_password_success(self, authenticated_client):
        """Test successful password change"""
        old_password = 'oldpass123'
        new_password = 'newpass456'
        
        # Set old password
        authenticated_client.user.set_password(old_password)
        authenticated_client.user.save()
        
        url = reverse('user-change-password')
        response = authenticated_client.post(url, {
            'old_password': old_password,
            'new_password': new_password,
            'new_password_confirm': new_password
        })
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify password was changed
        authenticated_client.user.refresh_from_db()
        assert authenticated_client.user.check_password(new_password)

    @pytest.mark.django_db
    def test_protected_endpoint_requires_auth(self, api_client):
        """Test that protected endpoints require authentication"""
        url = reverse('user-protected')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
