"""
Client for News Service
"""
from typing import Dict, Any, List, Optional
from .base_client import MicroserviceClient, MicroserviceError


class NewsServiceClient:
    """Client for News Service operations"""
    
    def __init__(self, client: MicroserviceClient):
        self.client = client
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """Get all news categories"""
        response = self.client.get('/api/news-categories')
        return response.get('categories', [])
    
    def create_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new news category"""
        response = self.client.post('/api/news-categories', data=category_data)
        return response
    
    def update_category(self, category_id: int, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update news category"""
        response = self.client.put(f'/api/news-categories/{category_id}', data=category_data)
        return response
    
    def delete_category(self, category_id: int) -> Dict[str, Any]:
        """Delete news category"""
        response = self.client.delete(f'/api/news-categories/{category_id}')
        return response
    
    def get_articles(self, category_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get all articles, optionally filtered by category"""
        params = {}
        if category_id:
            params['category_id'] = category_id
        
        response = self.client.get('/api/news-articles', params=params)
        return response.get('articles', [])
    
    def get_article(self, article_id: int) -> Dict[str, Any]:
        """Get specific article by ID"""
        response = self.client.get(f'/api/news-articles/{article_id}')
        return response
    
    def create_article(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new article"""
        response = self.client.post('/api/news-articles', data=article_data)
        return response
    
    def update_article(self, article_id: int, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update article"""
        response = self.client.put(f'/api/news-articles/{article_id}', data=article_data)
        return response
    
    def delete_article(self, article_id: int) -> Dict[str, Any]:
        """Delete article"""
        response = self.client.delete(f'/api/news-articles/{article_id}')
        return response
    
    def get_articles_by_category(self, category_id: int) -> List[Dict[str, Any]]:
        """Get articles by category"""
        response = self.client.get(f'/api/news/category/{category_id}/articles')
        return response.get('articles', [])
