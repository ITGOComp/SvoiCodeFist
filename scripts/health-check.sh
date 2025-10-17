#!/bin/bash

# Health check script for microservices

set -e

echo "🏥 Checking microservices health..."

# List of services to check
services=(
    "api-gateway:8000"
    "user-service:8001"
    "incident-service:8002"
    "traffic-service:8003"
    "news-service:8004"
    "chat-service:8005"
    "analytics-service:8006"
    "traffic-analytics-service:8007"
    "schedule-service:8008"
    "notification-service:8009"
)

# Function to check service health
check_service() {
    local service=$1
    local name=$(echo $service | cut -d: -f1)
    local port=$(echo $service | cut -d: -f2)
    
    echo -n "Checking $name... "
    
    if curl -f -s "http://localhost:$port/health" > /dev/null 2>&1; then
        echo "✅ Healthy"
        return 0
    else
        echo "❌ Unhealthy"
        return 1
    fi
}

# Check all services
failed_services=()
for service in "${services[@]}"; do
    if ! check_service "$service"; then
        failed_services+=("$service")
    fi
done

# Summary
echo ""
if [ ${#failed_services[@]} -eq 0 ]; then
    echo "🎉 All services are healthy!"
    exit 0
else
    echo "⚠️  Some services are unhealthy:"
    for service in "${failed_services[@]}"; do
        echo "  - $service"
    done
    echo ""
    echo "📋 To debug, check logs with:"
    for service in "${failed_services[@]}"; do
        name=$(echo $service | cut -d: -f1)
        echo "  docker-compose logs $name"
    done
    exit 1
fi

