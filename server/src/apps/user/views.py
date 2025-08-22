from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout, get_user_model

from apps.user.serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer,
    ChangePasswordSerializer
)
from apps import docs

User = get_user_model()

@docs.USER_VIEWSET_DOCS
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        elif self.action in ['list']:
            return [permissions.IsAdminUser()]
        
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action == 'login':
            return UserLoginSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return UserProfileSerializer

    @docs.USER_REGISTER_DOCS
    def create(self, request):
        """Register a new user"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'User registered successfully',
                'user': UserProfileSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @docs.USER_LOGIN_DOCS
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """Login user"""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            login(request, user)
            return Response({
                'message': 'Login successful',
                'user': UserProfileSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @docs.USER_LOGOUT_DOCS
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout user"""
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({
                    'error': 'Refresh token is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            return Response({
                'message': 'Successfully logged out'
            }, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)

    @docs.USER_PROFILE_DOCS
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user profile"""
        return Response({
            'message': f'Hello {request.user.email}! This is your profile.',
            'user': UserProfileSerializer(request.user).data
        })

    @docs.USER_CHANGE_PASSWORD_DOCS
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change user password"""
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({
                'message': 'Password changed successfully'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @docs.USER_PROTECTED_DOCS
    @action(detail=False, methods=['get'])
    def protected(self, request):
        """Example protected endpoint"""
        return Response({
            'message': f'Hello {request.user.email}! This is a protected endpoint.',
            'user_id': request.user.id,
            'username': request.user.username
        })

    def retrieve(self, request, *args, **kwargs):
        """Get user by ID or 'me' for current user"""
        if kwargs.get('pk') == 'me':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Update user profile"""
        if kwargs.get('pk') == 'me':
            kwargs['pk'] = request.user.id
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Partially update user profile"""
        if kwargs.get('pk') == 'me':
            kwargs['pk'] = request.user.id
        return super().partial_update(request, *args, **kwargs)


{
    "first_name": "Linda",
    "last_name": "Doe",
    "username": "linda",
    "email": "linda@example.com",
    "password": "senha123",
    "password_confirm": "senha123"
}
    

# last_name: Doe
# username: linda
# email: linda@example.com
# password: senha123
# password_confirm: senha123
