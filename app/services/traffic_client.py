"""
Client for Traffic Service
"""
from typing import Dict, Any, List, Optional
from .base_client import MicroserviceClient, MicroserviceError


class TrafficServiceClient:
    """Client for Traffic Service operations"""
    
    def __init__(self, client: MicroserviceClient):
        self.client = client
    
    def get_traffic_jams(self) -> List[Dict[str, Any]]:
        """Get all traffic jams"""
        response = self.client.get('/api/traffic')
        return response.get('traffic', [])
    
    def create_traffic_jam(self, traffic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new traffic jam"""
        response = self.client.post('/api/traffic', data=traffic_data)
        return response
    
    def get_patrols(self) -> List[Dict[str, Any]]:
        """Get all patrols"""
        response = self.client.get('/api/patrols')
        return response.get('patrols', [])
    
    def create_patrol(self, patrol_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new patrol"""
        response = self.client.post('/api/patrols', data=patrol_data)
        return response
    
    def get_cameras(self) -> List[Dict[str, Any]]:
        """Get all cameras"""
        response = self.client.get('/api/cameras')
        return response.get('cameras', [])
    
    def create_camera(self, camera_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new camera"""
        response = self.client.post('/api/cameras', data=camera_data)
        return response
    
    def get_detectors(self) -> List[Dict[str, Any]]:
        """Get all detectors"""
        response = self.client.get('/api/detectors')
        return response.get('detectors', [])
    
    def create_detector(self, detector_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new detector"""
        response = self.client.post('/api/detectors', data=detector_data)
        return response
    
    def ingest_detectors(self, file_data: bytes, filename: str) -> Dict[str, Any]:
        """Upload detectors from file"""
        # This would need special handling for file uploads
        # For now, return a placeholder
        return {"message": "File upload not implemented in base client"}
    
    def ingest_vehicle_passes(self, file_data: bytes, filename: str) -> Dict[str, Any]:
        """Upload vehicle passes from file"""
        # This would need special handling for file uploads
        return {"message": "File upload not implemented in base client"}
    
    def get_vehicle_path(self, vehicle_id: str, start: Optional[str] = None, end: Optional[str] = None) -> Dict[str, Any]:
        """Get vehicle path"""
        params = {'vehicle_id': vehicle_id}
        if start:
            params['start'] = start
        if end:
            params['end'] = end
        
        response = self.client.get('/api/traffic/vehicle-path', params=params)
        return response
    
    def get_comovement(self, vehicle_id: str, k: int = 3, dt: int = 300, max_lead: int = 2) -> Dict[str, Any]:
        """Get co-movement analysis"""
        params = {
            'vehicle_id': vehicle_id,
            'k': k,
            'dt': dt,
            'max_lead': max_lead
        }
        response = self.client.get('/api/traffic/comovement', params=params)
        return response
    
    def get_route_clusters(self, start: str, end: str, top: int = 10, min_len: int = 3) -> Dict[str, Any]:
        """Get route clusters"""
        params = {
            'start': start,
            'end': end,
            'top': top,
            'min_len': min_len
        }
        response = self.client.get('/api/traffic/cluster-routes', params=params)
        return response
    
    def snap_route(self, segments: List[List[List[float]]]) -> Dict[str, Any]:
        """Snap route to roads"""
        data = {'segments': segments}
        response = self.client.post('/api/traffic/route-snap', data=data)
        return response
