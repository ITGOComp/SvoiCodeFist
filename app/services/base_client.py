"""
Base client for microservices communication
"""
import requests
import json
import logging
from typing import Dict, Any, Optional, List
from django.conf import settings

logger = logging.getLogger(__name__)


class MicroserviceClient:
    """
    Base client for communicating with microservices
    """
    
    def __init__(self, service_name: str, base_url: str, timeout: int = 30):
        self.service_name = service_name
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _get_full_url(self, endpoint: str) -> str:
        """Construct full URL for the endpoint"""
        endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/{endpoint}"
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle HTTP response and convert to standard format"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error in {self.service_name}: {e}")
            raise MicroserviceError(f"HTTP {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error in {self.service_name}: {e}")
            raise MicroserviceError(f"Request failed: {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in {self.service_name}: {e}")
            raise MicroserviceError("Invalid JSON response")
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make GET request"""
        url = self._get_full_url(endpoint)
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"GET request failed for {self.service_name}: {e}")
            raise MicroserviceError(f"GET request failed: {str(e)}")
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make POST request"""
        url = self._get_full_url(endpoint)
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"POST request failed for {self.service_name}: {e}")
            raise MicroserviceError(f"POST request failed: {str(e)}")
    
    def put(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make PUT request"""
        url = self._get_full_url(endpoint)
        try:
            response = self.session.put(url, json=data, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"PUT request failed for {self.service_name}: {e}")
            raise MicroserviceError(f"PUT request failed: {str(e)}")
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request"""
        url = self._get_full_url(endpoint)
        try:
            response = self.session.delete(url, timeout=self.timeout)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"DELETE request failed for {self.service_name}: {e}")
            raise MicroserviceError(f"DELETE request failed: {str(e)}")
    
    def health_check(self) -> bool:
        """Check if service is healthy"""
        try:
            response = self.get('/health')
            return response.get('status') == 'healthy'
        except Exception:
            return False


class MicroserviceError(Exception):
    """Custom exception for microservice communication errors"""
    pass


class ServiceRegistry:
    """
    Registry for managing microservice clients
    """
    
    def __init__(self):
        self._clients = {}
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize all microservice clients"""
        # Get service URLs from settings
        service_urls = getattr(settings, 'MICROSERVICES', {})
        
        # Default service URLs (for development)
        default_urls = {
            'user_service': 'http://localhost:8001',
            'incident_service': 'http://localhost:8002',
            'traffic_service': 'http://localhost:8003',
            'news_service': 'http://localhost:8004',
            'chat_service': 'http://localhost:8005',
            'analytics_service': 'http://localhost:8006',
            'traffic_analytics_service': 'http://localhost:8007',
            'schedule_service': 'http://localhost:8008',
            'notification_service': 'http://localhost:8009',
        }
        
        # Use settings URLs or fallback to defaults
        urls = {**default_urls, **service_urls}
        
        for service_name, url in urls.items():
            self._clients[service_name] = MicroserviceClient(
                service_name=service_name,
                base_url=url
            )
    
    def get_client(self, service_name: str) -> MicroserviceClient:
        """Get client for specific service"""
        if service_name not in self._clients:
            raise ValueError(f"Service {service_name} not found")
        return self._clients[service_name]
    
    def get_all_clients(self) -> Dict[str, MicroserviceClient]:
        """Get all clients"""
        return self._clients.copy()
    
    def health_check_all(self) -> Dict[str, bool]:
        """Check health of all services"""
        health_status = {}
        for service_name, client in self._clients.items():
            health_status[service_name] = client.health_check()
        return health_status


# Global service registry instance
service_registry = ServiceRegistry()
