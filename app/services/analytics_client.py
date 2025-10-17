"""
Client for Analytics Service
"""
from typing import Dict, Any, List, Optional
from .base_client import MicroserviceClient, MicroserviceError


class AnalyticsServiceClient:
    """Client for Analytics Service operations"""
    
    def __init__(self, client: MicroserviceClient):
        self.client = client
    
    def get_accident_statistics(self) -> Dict[str, Any]:
        """Get accident statistics"""
        response = self.client.get('/api/analytics/accident-stats')
        return response
    
    def update_accident_statistics(self, stats_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update accident statistics"""
        response = self.client.post('/api/analytics/accident-stats', data=stats_data)
        return response
    
    def get_accident_types(self) -> List[Dict[str, Any]]:
        """Get accident types"""
        response = self.client.get('/api/analytics/accident-types')
        return response.get('types', [])
    
    def create_accident_type(self, type_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new accident type"""
        response = self.client.post('/api/analytics/accident-types', data=type_data)
        return response
    
    def update_accident_type(self, type_id: int, type_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update accident type"""
        response = self.client.put(f'/api/analytics/accident-types/{type_id}', data=type_data)
        return response
    
    def delete_accident_type(self, type_id: int) -> Dict[str, Any]:
        """Delete accident type"""
        response = self.client.delete(f'/api/analytics/accident-types/{type_id}')
        return response
    
    def get_accident_data(self, year: int = 2024) -> Dict[str, Any]:
        """Get accident data for specific year"""
        params = {'year': year}
        response = self.client.get('/api/analytics/accident-data', params=params)
        return response
    
    def update_accident_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update accident data"""
        response = self.client.post('/api/analytics/accident-data', data=data)
        return response
    
    def get_weather_data(self) -> Dict[str, Any]:
        """Get weather data"""
        response = self.client.get('/api/analytics/weather')
        return response
    
    def update_weather_data(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update weather data"""
        response = self.client.post('/api/analytics/weather', data=weather_data)
        return response
    
    def get_traffic_forecast(self) -> Dict[str, Any]:
        """Get traffic forecast"""
        response = self.client.get('/api/analytics/traffic-forecast')
        return response
    
    def update_traffic_forecast(self, forecast_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update traffic forecast"""
        response = self.client.post('/api/analytics/traffic-forecast', data=forecast_data)
        return response
    
    def get_road_works(self) -> Dict[str, Any]:
        """Get road works data"""
        response = self.client.get('/api/analytics/road-works')
        return response
    
    def update_road_works(self, works_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update road works data"""
        response = self.client.post('/api/analytics/road-works', data=works_data)
        return response
