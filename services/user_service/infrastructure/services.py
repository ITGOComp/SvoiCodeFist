"""
Infrastructure services for User Service
"""
import jwt
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional

from django.contrib.auth.hashers import make_password, check_password

from ..domain.entities import User
from ..domain.services import PasswordService, AuthenticationService, AuthorizationService


class DjangoPasswordService(PasswordService):
    """
    Django implementation of PasswordService
    """
    
    async def hash_password(self, password: str) -> str:
        """
        Hash password using Django's password hasher
        """
        return make_password(password)
    
    async def verify_password(self, password: str, hashed: str) -> bool:
        """
        Verify password against hash
        """
        return check_password(password, hashed)


class JWTService:
    """
    JWT token service
    """
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def generate_token(self, user: User, expires_in_hours: int = 24) -> str:
        """
        Generate JWT token for user
        """
        payload = {
            'user_id': user.id,
            'username': user.username,
            'role': user.role.value,
            'exp': datetime.utcnow() + timedelta(hours=expires_in_hours),
            'iat': datetime.utcnow()
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[dict]:
        """
        Verify JWT token and return payload
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None


class DjangoAuthenticationService(AuthenticationService):
    """
    Django implementation of AuthenticationService
    """
    
    def __init__(self, user_repository, password_service: PasswordService, jwt_service: JWTService):
        self.user_repository = user_repository
        self.password_service = password_service
        self.jwt_service = jwt_service
    
    async def authenticate(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate user with username and password
        """
        # Get user by username
        user = await self.user_repository.get_by_username(username)
        if not user:
            return None
        
        # Verify password
        # In real implementation, we would need to store hashed password
        # For now, this is a placeholder
        password_valid = True  # Placeholder
        
        if not password_valid:
            return None
        
        return user
    
    async def generate_token(self, user: User) -> str:
        """
        Generate JWT token for user
        """
        return self.jwt_service.generate_token(user)
    
    async def verify_token(self, token: str) -> Optional[User]:
        """
        Verify JWT token and return user
        """
        payload = self.jwt_service.verify_token(token)
        if not payload:
            return None
        
        user_id = payload.get('user_id')
        if not user_id:
            return None
        
        return await self.user_repository.get_by_id(user_id)


class DjangoAuthorizationService(AuthorizationService):
    """
    Django implementation of AuthorizationService
    """
    
    def __init__(self, permission_repository):
        self.permission_repository = permission_repository
    
    async def has_permission(self, user: User, resource: str, action: str) -> bool:
        """
        Check if user has permission for resource and action
        """
        # Admin has all permissions
        if user.is_admin():
            return True
        
        # Get user's role permissions
        permissions = await self.permission_repository.get_by_role(user.role.value)
        
        # Check if user has specific permission
        for permission in permissions:
            if permission.resource == resource and permission.action == action:
                return True
        
        return False
    
    async def can_access_resource(self, user: User, resource: str) -> bool:
        """
        Check if user can access resource
        """
        # Admin can access all resources
        if user.is_admin():
            return True
        
        # Get user's role permissions
        permissions = await self.permission_repository.get_by_role(user.role.value)
        
        # Check if user has any permission for resource
        for permission in permissions:
            if permission.resource == resource:
                return True
        
        return False

