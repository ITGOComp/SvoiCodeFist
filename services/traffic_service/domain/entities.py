"""
Domain entities for Traffic Service
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum


class TrafficJamSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PatrolStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"


class CameraStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


@dataclass
class TrafficJam:
    """
    Traffic jam domain entity
    """
    id: Optional[int]
    title: str
    description: str
    occurred_at: datetime
    coordinates: List[float]  # [latitude, longitude]
    severity: TrafficJamSeverity
    estimated_delay_minutes: Optional[int] = None
    affected_roads: Optional[List[str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def is_active(self) -> bool:
        # Traffic jam is considered active if it occurred within last 2 hours
        if not self.occurred_at:
            return False
        time_diff = datetime.now() - self.occurred_at
        return time_diff.total_seconds() < 7200  # 2 hours


@dataclass
class Patrol:
    """
    Patrol domain entity
    """
    id: Optional[int]
    title: str
    description: str
    coordinates: List[float]  # [latitude, longitude]
    radius_meters: int
    status: PatrolStatus
    assigned_officer: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def is_active(self) -> bool:
        return self.status == PatrolStatus.ACTIVE


@dataclass
class Camera:
    """
    Camera domain entity
    """
    id: Optional[int]
    name: str
    description: str
    coordinates: List[float]  # [latitude, longitude]
    status: CameraStatus
    stream_url: Optional[str] = None
    last_heartbeat: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def is_online(self) -> bool:
        return self.status == CameraStatus.ONLINE
    
    def is_heartbeat_recent(self, threshold_minutes: int = 5) -> bool:
        if not self.last_heartbeat:
            return False
        time_diff = datetime.now() - self.last_heartbeat
        return time_diff.total_seconds() < (threshold_minutes * 60)


@dataclass
class Detector:
    """
    Traffic detector domain entity
    """
    id: Optional[int]
    external_id: str
    name: str
    coordinates: List[float]  # [latitude, longitude]
    detector_type: str  # "induction_loop", "radar", "camera", etc.
    is_active: bool = True
    last_data_received: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def is_operational(self) -> bool:
        return self.is_active and self.last_data_received is not None


@dataclass
class VehiclePass:
    """
    Vehicle pass detection domain entity
    """
    id: Optional[int]
    detector_id: int
    vehicle_id: str
    timestamp: datetime
    speed_kmh: Optional[float] = None
    vehicle_type: Optional[str] = None
    lane: Optional[int] = None
    
    def is_speeding(self, speed_limit_kmh: float = 60) -> bool:
        return self.speed_kmh is not None and self.speed_kmh > speed_limit_kmh


@dataclass
class TrafficForecast:
    """
    Traffic forecast domain entity
    """
    id: Optional[int]
    location: str
    coordinates: List[float]  # [latitude, longitude]
    forecast_time: datetime
    predicted_speed_kmh: float
    confidence_level: float  # 0.0 to 1.0
    weather_conditions: Optional[str] = None
    road_conditions: Optional[str] = None
    created_at: Optional[datetime] = None
    
    def is_high_confidence(self) -> bool:
        return self.confidence_level >= 0.8


@dataclass
class RouteCluster:
    """
    Route cluster domain entity for traffic analytics
    """
    id: Optional[int]
    path: List[int]  # List of detector IDs
    start_time: datetime
    end_time: datetime
    vehicle_count: int
    avg_speed_kmh: Optional[float] = None
    avg_travel_seconds: Optional[float] = None
    created_at: Optional[datetime] = None
    
    def get_duration_hours(self) -> float:
        duration = self.end_time - self.start_time
        return duration.total_seconds() / 3600.0
    
    def get_intensity_per_hour(self) -> float:
        hours = self.get_duration_hours()
        return self.vehicle_count / hours if hours > 0 else 0

