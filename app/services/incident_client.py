"""
Client for Incident Service
"""
from typing import Dict, Any, List, Optional
from .base_client import MicroserviceClient, MicroserviceError


class IncidentServiceClient:
    """Client for Incident Service operations"""
    
    def __init__(self, client: MicroserviceClient):
        self.client = client
    
    def get_incidents(self, status: Optional[str] = None, severity: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all incidents with optional filtering"""
        params = {}
        if status:
            params['status'] = status
        if severity:
            params['severity'] = severity
        
        response = self.client.get('/api/incidents', params=params)
        return response.get('incidents', [])
    
    def get_incident(self, incident_id: int) -> Dict[str, Any]:
        """Get specific incident by ID"""
        response = self.client.get(f'/api/incidents/{incident_id}')
        return response
    
    def create_incident(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new incident"""
        response = self.client.post('/api/incidents', data=incident_data)
        return response
    
    def update_incident(self, incident_id: int, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update incident"""
        response = self.client.put(f'/api/incidents/{incident_id}', data=incident_data)
        return response
    
    def delete_incident(self, incident_id: int) -> Dict[str, Any]:
        """Delete incident"""
        response = self.client.delete(f'/api/incidents/{incident_id}')
        return response
    
    def get_appeals(self, filter_type: str = 'all') -> List[Dict[str, Any]]:
        """Get appeals with filtering"""
        params = {'filter': filter_type}
        response = self.client.get('/api/appeals', params=params)
        return response.get('appeals', [])
    
    def create_appeal(self, appeal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new appeal"""
        response = self.client.post('/api/appeals', data=appeal_data)
        return response
    
    def update_appeal(self, appeal_id: int, appeal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update appeal"""
        response = self.client.put(f'/api/appeals/{appeal_id}', data=appeal_data)
        return response
    
    def toggle_appeal_status(self, appeal_id: int) -> Dict[str, Any]:
        """Toggle appeal review status"""
        response = self.client.post(f'/api/appeals/{appeal_id}/toggle')
        return response
    
    def get_incident_statistics(self) -> Dict[str, Any]:
        """Get incident statistics"""
        response = self.client.get('/api/incidents/statistics')
        return response
