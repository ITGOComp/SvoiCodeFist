"""
API Gateway for microservices architecture
"""
import asyncio
import aiohttp
import json
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Traffic Monitoring API Gateway",
    description="API Gateway for traffic monitoring microservices",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

# Service configurations
SERVICES = {
    "user_service": {
        "url": "http://user-service:8001",
        "health_check": "/health",
        "timeout": 30
    },
    "incident_service": {
        "url": "http://incident-service:8002",
        "health_check": "/health",
        "timeout": 30
    },
    "traffic_service": {
        "url": "http://traffic-service:8003",
        "health_check": "/health",
        "timeout": 30
    },
    "news_service": {
        "url": "http://news-service:8004",
        "health_check": "/health",
        "timeout": 30
    },
    "chat_service": {
        "url": "http://chat-service:8005",
        "health_check": "/health",
        "timeout": 30
    },
    "analytics_service": {
        "url": "http://analytics-service:8006",
        "health_check": "/health",
        "timeout": 30
    },
    "traffic_analytics_service": {
        "url": "http://traffic-analytics-service:8007",
        "health_check": "/health",
        "timeout": 30
    },
    "schedule_service": {
        "url": "http://schedule-service:8008",
        "health_check": "/health",
        "timeout": 30
    },
    "notification_service": {
        "url": "http://notification-service:8009",
        "health_check": "/health",
        "timeout": 30
    }
}

# Route mappings
ROUTE_MAPPINGS = {
    "/api/users": "user_service",
    "/api/auth": "user_service",
    "/api/incidents": "incident_service",
    "/api/appeals": "incident_service",
    "/api/traffic": "traffic_service",
    "/api/patrols": "traffic_service",
    "/api/cameras": "traffic_service",
    "/api/detectors": "traffic_service",
    "/api/news": "news_service",
    "/api/chat": "chat_service",
    "/api/analytics": "analytics_service",
    "/api/traffic-analytics": "traffic_analytics_service",
    "/api/schedule": "schedule_service",
    "/api/notifications": "notification_service"
}


class ServiceClient:
    """
    HTTP client for service communication
    """
    
    def __init__(self):
        self.session = None
    
    async def get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close(self):
        if self.session:
            await self.session.close()
    
    async def make_request(
        self,
        service_name: str,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to a service
        """
        if service_name not in SERVICES:
            raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
        
        service_config = SERVICES[service_name]
        url = f"{service_config['url']}{path}"
        
        session = await self.get_session()
        
        try:
            async with session.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=service_config['timeout'])
            ) as response:
                response_data = await response.json()
                
                if response.status >= 400:
                    raise HTTPException(
                        status_code=response.status,
                        detail=response_data.get('detail', 'Service error')
                    )
                
                return response_data
                
        except aiohttp.ClientError as e:
            logger.error(f"Service communication error: {e}")
            raise HTTPException(status_code=503, detail="Service unavailable")
        except asyncio.TimeoutError:
            logger.error(f"Service timeout: {service_name}")
            raise HTTPException(status_code=504, detail="Service timeout")


# Global service client
service_client = ServiceClient()


def get_service_for_path(path: str) -> Optional[str]:
    """
    Determine which service should handle the request based on path
    """
    for route_prefix, service_name in ROUTE_MAPPINGS.items():
        if path.startswith(route_prefix):
            return service_name
    return None


@app.middleware("http")
async def service_routing_middleware(request: Request, call_next):
    """
    Middleware to route requests to appropriate services
    """
    path = request.url.path
    
    # Skip health checks and docs
    if path in ["/health", "/docs", "/openapi.json", "/"]:
        return await call_next(request)
    
    # Determine target service
    service_name = get_service_for_path(path)
    
    if not service_name:
        return JSONResponse(
            status_code=404,
            content={"detail": "Route not found"}
        )
    
    # Forward request to service
    try:
        # Prepare request data
        data = None
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                data = await request.json()
            except:
                pass
        
        # Prepare headers
        headers = dict(request.headers)
        # Remove host header to avoid conflicts
        headers.pop("host", None)
        
        # Make request to service
        response_data = await service_client.make_request(
            service_name=service_name,
            method=request.method,
            path=path,
            data=data,
            headers=headers
        )
        
        return JSONResponse(content=response_data)
        
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except Exception as e:
        logger.error(f"Gateway error: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal gateway error"}
        )


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "service": "api_gateway"}


@app.get("/services/health")
async def services_health_check():
    """
    Check health of all services
    """
    health_status = {}
    
    for service_name, config in SERVICES.items():
        try:
            response_data = await service_client.make_request(
                service_name=service_name,
                method="GET",
                path=config["health_check"]
            )
            health_status[service_name] = {
                "status": "healthy",
                "response": response_data
            }
        except Exception as e:
            health_status[service_name] = {
                "status": "unhealthy",
                "error": str(e)
            }
    
    return {"services": health_status}


@app.on_event("startup")
async def startup_event():
    """
    Startup event handler
    """
    logger.info("API Gateway starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler
    """
    await service_client.close()
    logger.info("API Gateway shutting down...")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

