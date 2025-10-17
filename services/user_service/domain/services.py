"""
Domain services for User Service
"""
from abc import ABC, abstractmethod
from typing import Optional
from .entities import User, UserRole, UserStatus


class PasswordService(ABC):
    """
    Password service interface
    """
    
    @abstractmethod
    async def hash_password(self, password: str) -> str:
        pass
    
    @abstractmethod
    async def verify_password(self, password: str, hashed: str) -> bool:
        pass


class AuthenticationService(ABC):
    """
    Authentication service interface
    """
    
    @abstractmethod
    async def authenticate(self, username: str, password: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def generate_token(self, user: User) -> str:
        pass
    
    @abstractmethod
    async def verify_token(self, token: str) -> Optional[User]:
        pass


class AuthorizationService(ABC):
    """
    Authorization service interface
    """
    
    @abstractmethod
    async def has_permission(self, user: User, resource: str, action: str) -> bool:
        pass
    
    @abstractmethod
    async def can_access_resource(self, user: User, resource: str) -> bool:
        pass


class UserDomainService:
    """
    User domain service
    """
    
    def __init__(self, password_service: PasswordService):
        self.password_service = password_service
    
    async def create_user(
        self,
        username: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        role: UserRole = UserRole.USER
    ) -> User:
        """
        Create a new user with business rules validation
        """
        # Validate username format
        if not self._is_valid_username(username):
            raise ValueError("Invalid username format")
        
        # Validate email format
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")
        
        # Validate password strength
        if not self._is_strong_password(password):
            raise ValueError("Password does not meet security requirements")
        
        # Hash password
        hashed_password = await self.password_service.hash_password(password)
        
        # Create user entity
        user = User(
            id=None,
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            status=UserStatus.PENDING,
            created_at=None,  # Will be set by repository
            updated_at=None,  # Will be set by repository
            is_verified=False
        )
        
        return user
    
    def _is_valid_username(self, username: str) -> bool:
        """
        Validate username format
        """
        if not username or len(username) < 3 or len(username) > 30:
            return False
        
        # Username should contain only alphanumeric characters and underscores
        return username.replace('_', '').isalnum()
    
    def _is_valid_email(self, email: str) -> bool:
        """
        Validate email format
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _is_strong_password(self, password: str) -> bool:
        """
        Validate password strength
        """
        if len(password) < 8:
            return False
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        return has_upper and has_lower and has_digit and has_special

