#!/bin/bash

# Deploy script for microservices architecture

set -e

echo "🚀 Starting deployment of microservices architecture..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p data
mkdir -p monitoring/grafana/dashboards
mkdir -p monitoring/grafana/datasources
mkdir -p monitoring/logstash/pipeline
mkdir -p monitoring/logstash/config

# Set environment variables
export COMPOSE_PROJECT_NAME=traffic-monitoring
export ENVIRONMENT=development

# Build and start services
echo "🔨 Building and starting services..."
docker-compose down --remove-orphans
docker-compose build --no-cache
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🏥 Checking service health..."
./scripts/health-check.sh

# Run database migrations
echo "🗄️ Running database migrations..."
docker-compose exec user-service python manage.py migrate
docker-compose exec incident-service python manage.py migrate
docker-compose exec traffic-service python manage.py migrate
docker-compose exec news-service python manage.py migrate
docker-compose exec chat-service python manage.py migrate
docker-compose exec analytics-service python manage.py migrate
docker-compose exec traffic-analytics-service python manage.py migrate
docker-compose exec schedule-service python manage.py migrate
docker-compose exec notification-service python manage.py migrate

# Create superuser for admin access
echo "👤 Creating admin user..."
docker-compose exec user-service python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 Services are available at:"
echo "  - API Gateway: http://localhost:8000"
echo "  - Grafana: http://localhost:3000 (admin/admin)"
echo "  - Prometheus: http://localhost:9090"
echo "  - Kibana: http://localhost:5601"
echo "  - RabbitMQ Management: http://localhost:15672 (admin/password)"
echo ""
echo "📊 To view logs: docker-compose logs -f [service-name]"
echo "🛑 To stop services: docker-compose down"

