"""
Service Manager for coordinating all microservices
"""
from typing import Dict, Any, Optional
from .base_client import service_registry, MicroserviceError
from .incident_client import IncidentServiceClient
from .traffic_client import TrafficServiceClient
from .news_client import NewsServiceClient
from .chat_client import ChatServiceClient
from .analytics_client import AnalyticsServiceClient


class ServiceManager:
    """
    Main service manager for coordinating all microservices
    """
    
    def __init__(self):
        self.registry = service_registry
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize all service clients"""
        # Get base clients
        incident_client = self.registry.get_client('incident_service')
        traffic_client = self.registry.get_client('traffic_service')
        news_client = self.registry.get_client('news_service')
        chat_client = self.registry.get_client('chat_service')
        analytics_client = self.registry.get_client('analytics_service')
        
        # Create specialized clients
        self.incident = IncidentServiceClient(incident_client)
        self.traffic = TrafficServiceClient(traffic_client)
        self.news = NewsServiceClient(news_client)
        self.chat = ChatServiceClient(chat_client)
        self.analytics = AnalyticsServiceClient(analytics_client)
    
    def health_check_all(self) -> Dict[str, bool]:
        """Check health of all services"""
        return self.registry.health_check_all()
    
    def is_service_available(self, service_name: str) -> bool:
        """Check if specific service is available"""
        try:
            client = self.registry.get_client(service_name)
            return client.health_check()
        except Exception:
            return False
    
    def get_service_status(self) -> Dict[str, Dict[str, Any]]:
        """Get detailed status of all services"""
        status = {}
        health_status = self.health_check_all()
        
        for service_name, is_healthy in health_status.items():
            status[service_name] = {
                'healthy': is_healthy,
                'available': self.is_service_available(service_name),
                'url': self.registry.get_client(service_name).base_url
            }
        
        return status


# Global service manager instance
service_manager = ServiceManager()
