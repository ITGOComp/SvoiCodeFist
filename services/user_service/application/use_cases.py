"""
Use cases for User Service
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime

from ..domain.entities import User, UserSession, UserRole, UserStatus
from ..domain.repositories import UserRepository, UserSessionRepository
from ..domain.services import PasswordService, AuthenticationService, AuthorizationService


@dataclass
class CreateUserRequest:
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    role: UserRole = UserRole.USER


@dataclass
class CreateUserResponse:
    user: User
    success: bool
    message: str


@dataclass
class AuthenticateUserRequest:
    username: str
    password: str


@dataclass
class AuthenticateUserResponse:
    user: Optional[User]
    token: Optional[str]
    success: bool
    message: str


@dataclass
class GetUserRequest:
    user_id: int


@dataclass
class GetUserResponse:
    user: Optional[User]
    success: bool
    message: str


class CreateUserUseCase:
    """
    Use case for creating a new user
    """
    
    def __init__(
        self,
        user_repository: UserRepository,
        password_service: PasswordService
    ):
        self.user_repository = user_repository
        self.password_service = password_service
    
    async def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        """
        Execute create user use case
        """
        try:
            # Check if user already exists
            existing_user = await self.user_repository.get_by_username(request.username)
            if existing_user:
                return CreateUserResponse(
                    user=None,
                    success=False,
                    message="Username already exists"
                )
            
            existing_email = await self.user_repository.get_by_email(request.email)
            if existing_email:
                return CreateUserResponse(
                    user=None,
                    success=False,
                    message="Email already exists"
                )
            
            # Create user using domain service
            from ..domain.services import UserDomainService
            user_domain_service = UserDomainService(self.password_service)
            
            user = await user_domain_service.create_user(
                username=request.username,
                email=request.email,
                password=request.password,
                first_name=request.first_name,
                last_name=request.last_name,
                role=request.role
            )
            
            # Save to repository
            created_user = await self.user_repository.create(user)
            
            return CreateUserResponse(
                user=created_user,
                success=True,
                message="User created successfully"
            )
            
        except ValueError as e:
            return CreateUserResponse(
                user=None,
                success=False,
                message=str(e)
            )
        except Exception as e:
            return CreateUserResponse(
                user=None,
                success=False,
                message=f"Internal error: {str(e)}"
            )


class AuthenticateUserUseCase:
    """
    Use case for user authentication
    """
    
    def __init__(
        self,
        user_repository: UserRepository,
        session_repository: UserSessionRepository,
        authentication_service: AuthenticationService
    ):
        self.user_repository = user_repository
        self.session_repository = session_repository
        self.authentication_service = authentication_service
    
    async def execute(self, request: AuthenticateUserRequest) -> AuthenticateUserResponse:
        """
        Execute authenticate user use case
        """
        try:
            # Authenticate user
            user = await self.authentication_service.authenticate(
                request.username,
                request.password
            )
            
            if not user:
                return AuthenticateUserResponse(
                    user=None,
                    token=None,
                    success=False,
                    message="Invalid credentials"
                )
            
            if not user.is_active():
                return AuthenticateUserResponse(
                    user=None,
                    token=None,
                    success=False,
                    message="User account is not active"
                )
            
            # Generate token
            token = await self.authentication_service.generate_token(user)
            
            # Create session
            session = UserSession(
                id=f"session_{user.id}_{datetime.now().timestamp()}",
                user_id=user.id,
                token=token,
                expires_at=datetime.now().replace(hour=23, minute=59, second=59),
                created_at=datetime.now(),
                is_active=True
            )
            
            await self.session_repository.create(session)
            
            return AuthenticateUserResponse(
                user=user,
                token=token,
                success=True,
                message="Authentication successful"
            )
            
        except Exception as e:
            return AuthenticateUserResponse(
                user=None,
                token=None,
                success=False,
                message=f"Internal error: {str(e)}"
            )


class GetUserUseCase:
    """
    Use case for getting user by ID
    """
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def execute(self, request: GetUserRequest) -> GetUserResponse:
        """
        Execute get user use case
        """
        try:
            user = await self.user_repository.get_by_id(request.user_id)
            
            if not user:
                return GetUserResponse(
                    user=None,
                    success=False,
                    message="User not found"
                )
            
            return GetUserResponse(
                user=user,
                success=True,
                message="User retrieved successfully"
            )
            
        except Exception as e:
            return GetUserResponse(
                user=None,
                success=False,
                message=f"Internal error: {str(e)}"
            )


class ListUsersUseCase:
    """
    Use case for listing users
    """
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def execute(self, limit: int = 100, offset: int = 0) -> List[User]:
        """
        Execute list users use case
        """
        return await self.user_repository.list_users(limit, offset)


class UpdateUserUseCase:
    """
    Use case for updating user
    """
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def execute(self, user: User) -> User:
        """
        Execute update user use case
        """
        return await self.user_repository.update(user)


class DeleteUserUseCase:
    """
    Use case for deleting user
    """
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def execute(self, user_id: int) -> bool:
        """
        Execute delete user use case
        """
        return await self.user_repository.delete(user_id)

