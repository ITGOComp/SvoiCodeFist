"""
Repository interfaces for User Service
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from .entities import User, UserSession, Permission, Role


class UserRepository(ABC):
    """
    User repository interface
    """
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def create(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        pass
    
    @abstractmethod
    async def list_users(self, limit: int = 100, offset: int = 0) -> List[User]:
        pass
    
    @abstractmethod
    async def search_users(self, query: str, limit: int = 100) -> List[User]:
        pass


class UserSessionRepository(ABC):
    """
    User session repository interface
    """
    
    @abstractmethod
    async def get_by_token(self, token: str) -> Optional[UserSession]:
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> List[UserSession]:
        pass
    
    @abstractmethod
    async def create(self, session: UserSession) -> UserSession:
        pass
    
    @abstractmethod
    async def update(self, session: UserSession) -> UserSession:
        pass
    
    @abstractmethod
    async def delete(self, session_id: str) -> bool:
        pass
    
    @abstractmethod
    async def delete_expired_sessions(self) -> int:
        pass


class PermissionRepository(ABC):
    """
    Permission repository interface
    """
    
    @abstractmethod
    async def get_by_id(self, permission_id: int) -> Optional[Permission]:
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Permission]:
        pass
    
    @abstractmethod
    async def list_permissions(self) -> List[Permission]:
        pass
    
    @abstractmethod
    async def get_by_role(self, role_name: str) -> List[Permission]:
        pass


class RoleRepository(ABC):
    """
    Role repository interface
    """
    
    @abstractmethod
    async def get_by_id(self, role_id: int) -> Optional[Role]:
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Role]:
        pass
    
    @abstractmethod
    async def list_roles(self) -> List[Role]:
        pass

