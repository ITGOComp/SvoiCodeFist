"""
Controllers for User Service
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from ..application.use_cases import (
    CreateUserUseCase, AuthenticateUserUseCase, GetUserUseCase,
    ListUsersUseCase, UpdateUserUseCase, DeleteUserUseCase,
    CreateUserRequest, AuthenticateUserRequest, GetUserRequest
)
from ..domain.entities import UserRole
from ..infrastructure.repositories import (
    DjangoUserRepository, DjangoUserSessionRepository,
    DjangoPermissionRepository, DjangoRoleRepository
)
from ..infrastructure.services import (
    DjangoPasswordService, DjangoAuthenticationService,
    DjangoAuthorizationService, JWTService
)


class UserController(APIView):
    """
    User management controller
    """
    
    def __init__(self):
        # Initialize repositories and services
        self.user_repository = DjangoUserRepository()
        self.session_repository = DjangoUserSessionRepository()
        self.permission_repository = DjangoPermissionRepository()
        self.role_repository = DjangoRoleRepository()
        
        self.password_service = DjangoPasswordService()
        self.jwt_service = JWTService(secret_key="your-secret-key")
        self.auth_service = DjangoAuthenticationService(
            self.user_repository, self.password_service, self.jwt_service
        )
        self.authorization_service = DjangoAuthorizationService(self.permission_repository)
        
        # Initialize use cases
        self.create_user_use_case = CreateUserUseCase(
            self.user_repository, self.password_service
        )
        self.authenticate_user_use_case = AuthenticateUserUseCase(
            self.user_repository, self.session_repository, self.auth_service
        )
        self.get_user_use_case = GetUserUseCase(self.user_repository)
        self.list_users_use_case = ListUsersUseCase(self.user_repository)
        self.update_user_use_case = UpdateUserUseCase(self.user_repository)
        self.delete_user_use_case = DeleteUserUseCase(self.user_repository)
    
    @api_view(['POST'])
    @permission_classes([AllowAny])
    def create_user(self, request):
        """
        Create a new user
        """
        try:
            data = request.data
            
            # Validate required fields
            required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
            for field in required_fields:
                if field not in data:
                    return Response(
                        {'error': f'Field {field} is required'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Create request object
            create_request = CreateUserRequest(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                role=UserRole(data.get('role', 'user'))
            )
            
            # Execute use case
            response = await self.create_user_use_case.execute(create_request)
            
            if response.success:
                return Response(
                    {
                        'message': response.message,
                        'user': {
                            'id': response.user.id,
                            'username': response.user.username,
                            'email': response.user.email,
                            'first_name': response.user.first_name,
                            'last_name': response.user.last_name,
                            'role': response.user.role.value,
                            'status': response.user.status.value
                        }
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'error': response.message},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            return Response(
                {'error': f'Internal server error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @api_view(['POST'])
    @permission_classes([AllowAny])
    def authenticate_user(self, request):
        """
        Authenticate user
        """
        try:
            data = request.data
            
            # Validate required fields
            if 'username' not in data or 'password' not in data:
                return Response(
                    {'error': 'Username and password are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create request object
            auth_request = AuthenticateUserRequest(
                username=data['username'],
                password=data['password']
            )
            
            # Execute use case
            response = await self.authenticate_user_use_case.execute(auth_request)
            
            if response.success:
                return Response(
                    {
                        'message': response.message,
                        'token': response.token,
                        'user': {
                            'id': response.user.id,
                            'username': response.user.username,
                            'email': response.user.email,
                            'first_name': response.user.first_name,
                            'last_name': response.user.last_name,
                            'role': response.user.role.value,
                            'status': response.user.status.value
                        }
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': response.message},
                    status=status.HTTP_401_UNAUTHORIZED
                )
                
        except Exception as e:
            return Response(
                {'error': f'Internal server error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def get_user(self, request, user_id):
        """
        Get user by ID
        """
        try:
            # Create request object
            get_request = GetUserRequest(user_id=int(user_id))
            
            # Execute use case
            response = await self.get_user_use_case.execute(get_request)
            
            if response.success:
                return Response(
                    {
                        'message': response.message,
                        'user': {
                            'id': response.user.id,
                            'username': response.user.username,
                            'email': response.user.email,
                            'first_name': response.user.first_name,
                            'last_name': response.user.last_name,
                            'role': response.user.role.value,
                            'status': response.user.status.value,
                            'created_at': response.user.created_at.isoformat() if response.user.created_at else None,
                            'updated_at': response.user.updated_at.isoformat() if response.user.updated_at else None
                        }
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': response.message},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except ValueError:
            return Response(
                {'error': 'Invalid user ID'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Internal server error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def list_users(self, request):
        """
        List users with pagination
        """
        try:
            limit = int(request.GET.get('limit', 100))
            offset = int(request.GET.get('offset', 0))
            
            # Execute use case
            users = await self.list_users_use_case.execute(limit, offset)
            
            user_list = []
            for user in users:
                user_list.append({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role.value,
                    'status': user.status.value,
                    'created_at': user.created_at.isoformat() if user.created_at else None
                })
            
            return Response(
                {
                    'users': user_list,
                    'count': len(user_list)
                },
                status=status.HTTP_200_OK
            )
            
        except ValueError:
            return Response(
                {'error': 'Invalid pagination parameters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Internal server error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    def update_user(self, request, user_id):
        """
        Update user
        """
        try:
            # Get existing user
            get_request = GetUserRequest(user_id=int(user_id))
            get_response = await self.get_user_use_case.execute(get_request)
            
            if not get_response.success:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            user = get_response.user
            data = request.data
            
            # Update user fields
            if 'first_name' in data:
                user.first_name = data['first_name']
            if 'last_name' in data:
                user.last_name = data['last_name']
            if 'email' in data:
                user.email = data['email']
            if 'role' in data:
                user.role = UserRole(data['role'])
            if 'status' in data:
                user.status = UserStatus(data['status'])
            
            # Execute use case
            updated_user = await self.update_user_use_case.execute(user)
            
            return Response(
                {
                    'message': 'User updated successfully',
                    'user': {
                        'id': updated_user.id,
                        'username': updated_user.username,
                        'email': updated_user.email,
                        'first_name': updated_user.first_name,
                        'last_name': updated_user.last_name,
                        'role': updated_user.role.value,
                        'status': updated_user.status.value,
                        'updated_at': updated_user.updated_at.isoformat() if updated_user.updated_at else None
                    }
                },
                status=status.HTTP_200_OK
            )
            
        except ValueError:
            return Response(
                {'error': 'Invalid user ID or data'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Internal server error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    def delete_user(self, request, user_id):
        """
        Delete user
        """
        try:
            # Execute use case
            success = await self.delete_user_use_case.execute(int(user_id))
            
            if success:
                return Response(
                    {'message': 'User deleted successfully'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except ValueError:
            return Response(
                {'error': 'Invalid user ID'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Internal server error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

