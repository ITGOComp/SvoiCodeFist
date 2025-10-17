"""
Domain entities for User Service
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    USER = "user"
    GUEST = "guest"


class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


@dataclass
class User:
    """
    User domain entity
    """
    id: Optional[int]
    username: str
    email: str
    first_name: str
    last_name: str
    role: UserRole
    status: UserStatus
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    is_verified: bool = False
    
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN
    
    def is_editor(self) -> bool:
        return self.role in [UserRole.ADMIN, UserRole.EDITOR]
    
    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE
    
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()


@dataclass
class UserSession:
    """
    User session domain entity
    """
    id: str
    user_id: int
    token: str
    expires_at: datetime
    created_at: datetime
    is_active: bool = True
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


@dataclass
class Permission:
    """
    Permission domain entity
    """
    id: int
    name: str
    description: str
    resource: str
    action: str


@dataclass
class Role:
    """
    Role domain entity
    """
    id: int
    name: str
    description: str
    permissions: List[Permission]

