"""
Domain entities for Incident Service
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum


class IncidentStatus(Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class IncidentSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AppealStatus(Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


@dataclass
class Incident:
    """
    Incident domain entity
    """
    id: Optional[int]
    title: str
    description: str
    occurred_at: datetime
    status: IncidentStatus
    severity: IncidentSeverity
    coordinates: List[float]  # [latitude, longitude]
    related_appeal_id: Optional[int] = None
    assigned_to: Optional[int] = None  # User ID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    
    def is_resolved(self) -> bool:
        return self.status in [IncidentStatus.RESOLVED, IncidentStatus.CLOSED]
    
    def is_high_priority(self) -> bool:
        return self.severity in [IncidentSeverity.HIGH, IncidentSeverity.CRITICAL]
    
    def can_be_assigned(self) -> bool:
        return self.status == IncidentStatus.NEW


@dataclass
class Appeal:
    """
    Appeal domain entity
    """
    id: Optional[int]
    name: str
    email: str
    message: str
    status: AppealStatus
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[int] = None  # User ID
    
    def is_pending(self) -> bool:
        return self.status == AppealStatus.PENDING
    
    def can_be_reviewed(self) -> bool:
        return self.status == AppealStatus.PENDING


@dataclass
class IncidentComment:
    """
    Incident comment domain entity
    """
    id: Optional[int]
    incident_id: int
    user_id: int
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class IncidentAttachment:
    """
    Incident attachment domain entity
    """
    id: Optional[int]
    incident_id: int
    filename: str
    file_path: str
    file_size: int
    mime_type: str
    uploaded_by: int  # User ID
    created_at: Optional[datetime] = None

