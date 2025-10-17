"""
Client for Chat Service
"""
from typing import Dict, Any, List, Optional
from .base_client import MicroserviceClient, MicroserviceError


class ChatServiceClient:
    """Client for Chat Service operations"""
    
    def __init__(self, client: MicroserviceClient):
        self.client = client
    
    def send_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send chat message"""
        response = self.client.post('/api/chat/send', data=message_data)
        return response
    
    def get_messages(self, thread_id: Optional[int] = None) -> Dict[str, Any]:
        """Get chat messages for thread"""
        params = {}
        if thread_id:
            params['thread_id'] = thread_id
        
        response = self.client.get('/api/chat/messages', params=params)
        return response
    
    def get_threads(self) -> List[Dict[str, Any]]:
        """Get all chat threads"""
        response = self.client.get('/api/chat-threads')
        return response.get('threads', [])
    
    def get_admin_threads(self) -> List[Dict[str, Any]]:
        """Get all chat threads for admin"""
        response = self.client.get('/api/admin/chat-threads')
        return response.get('threads', [])
    
    def toggle_thread_status(self, thread_id: int) -> Dict[str, Any]:
        """Toggle thread open/closed status"""
        response = self.client.post(f'/api/chat-threads/{thread_id}/toggle')
        return response
    
    def create_thread(self, thread_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new chat thread"""
        response = self.client.post('/api/chat-threads', data=thread_data)
        return response
    
    def get_thread(self, thread_id: int) -> Dict[str, Any]:
        """Get specific thread by ID"""
        response = self.client.get(f'/api/chat-threads/{thread_id}')
        return response
