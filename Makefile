# Makefile for Traffic Monitoring Microservices

.PHONY: help build up down restart logs clean deploy health-check backup restore

# Default target
help: ## Show this help message
	@echo "Traffic Monitoring Microservices - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Build and run services
build: ## Build all Docker images
	docker-compose build --no-cache

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

restart: ## Restart all services
	docker-compose restart

# Development commands
dev: ## Start services in development mode with logs
	docker-compose up

logs: ## Show logs for all services
	docker-compose logs -f

logs-service: ## Show logs for specific service (usage: make logs-service SERVICE=user-service)
	docker-compose logs -f $(SERVICE)

# Database commands
migrate: ## Run database migrations for all services
	docker-compose exec user-service python manage.py migrate
	docker-compose exec incident-service python manage.py migrate
	docker-compose exec traffic-service python manage.py migrate
	docker-compose exec news-service python manage.py migrate
	docker-compose exec chat-service python manage.py migrate
	docker-compose exec analytics-service python manage.py migrate
	docker-compose exec traffic-analytics-service python manage.py migrate
	docker-compose exec schedule-service python manage.py migrate
	docker-compose exec notification-service python manage.py migrate

migrate-service: ## Run migrations for specific service (usage: make migrate-service SERVICE=user-service)
	docker-compose exec $(SERVICE) python manage.py migrate

createsuperuser: ## Create superuser for user service
	docker-compose exec user-service python manage.py createsuperuser

# Monitoring and health
health-check: ## Check health of all services
	@echo "Checking service health..."
	@for service in api-gateway:9000 user-service:8001 incident-service:8002 traffic-service:8003 news-service:8004 chat-service:8005 analytics-service:8006 traffic-analytics-service:8007 schedule-service:8008 notification-service:8009; do \
		name=$$(echo $$service | cut -d: -f1); \
		port=$$(echo $$service | cut -d: -f2); \
		echo -n "Checking $$name... "; \
		if curl -f -s "http://localhost:$$port/health" > /dev/null 2>&1; then \
			echo "✅ Healthy"; \
		else \
			echo "❌ Unhealthy"; \
		fi; \
	done

status: ## Show status of all services
	docker-compose ps

# Backup and restore
backup: ## Create backup of all databases
	./scripts/backup.sh

restore: ## Restore from backup (usage: make restore BACKUP=backup_file.tar.gz)
	./scripts/restore.sh $(BACKUP)

# Cleanup commands
clean: ## Remove all containers, networks, and volumes
	docker-compose down -v --remove-orphans
	docker system prune -f

clean-images: ## Remove all Docker images
	docker-compose down --rmi all

clean-volumes: ## Remove all volumes
	docker-compose down -v

# Scaling commands
scale: ## Scale specific service (usage: make scale SERVICE=user-service REPLICAS=3)
	docker-compose up -d --scale $(SERVICE)=$(REPLICAS)

# Service-specific commands
shell: ## Open shell in specific service (usage: make shell SERVICE=user-service)
	docker-compose exec $(SERVICE) /bin/bash

shell-db: ## Open database shell (usage: make shell-db SERVICE=user-db)
	docker-compose exec $(SERVICE) psql -U user -d $(shell echo $(SERVICE) | sed 's/-db//g')_service

# Testing commands
test: ## Run tests for all services
	docker-compose exec user-service python manage.py test
	docker-compose exec incident-service python manage.py test
	docker-compose exec traffic-service python manage.py test
	docker-compose exec news-service python manage.py test
	docker-compose exec chat-service python manage.py test
	docker-compose exec analytics-service python manage.py test
	docker-compose exec traffic-analytics-service python manage.py test
	docker-compose exec schedule-service python manage.py test
	docker-compose exec notification-service python manage.py test

test-service: ## Run tests for specific service (usage: make test-service SERVICE=user-service)
	docker-compose exec $(SERVICE) python manage.py test

# Production deployment
deploy: ## Deploy to production
	./scripts/deploy.sh

# Monitoring access
grafana: ## Open Grafana in browser
	@echo "Opening Grafana at http://localhost:3000"
	@echo "Username: admin, Password: admin"
	@if command -v xdg-open > /dev/null; then xdg-open http://localhost:3000; \
	elif command -v open > /dev/null; then open http://localhost:3000; \
	else echo "Please open http://localhost:3000 in your browser"; fi

prometheus: ## Open Prometheus in browser
	@echo "Opening Prometheus at http://localhost:9090"
	@if command -v xdg-open > /dev/null; then xdg-open http://localhost:9090; \
	elif command -v open > /dev/null; then open http://localhost:9090; \
	else echo "Please open http://localhost:9090 in your browser"; fi

kibana: ## Open Kibana in browser
	@echo "Opening Kibana at http://localhost:5601"
	@if command -v xdg-open > /dev/null; then xdg-open http://localhost:5601; \
	elif command -v open > /dev/null; then open http://localhost:5601; \
	else echo "Please open http://localhost:5601 in your browser"; fi

rabbitmq: ## Open RabbitMQ Management in browser
	@echo "Opening RabbitMQ Management at http://localhost:15672"
	@echo "Username: admin, Password: password"
	@if command -v xdg-open > /dev/null; then xdg-open http://localhost:15672; \
	elif command -v open > /dev/null; then open http://localhost:15672; \
	else echo "Please open http://localhost:15672 in your browser"; fi

# Quick start
start: build up migrate health-check ## Quick start: build, up, migrate, and health check
	@echo "✅ All services are up and running!"
	@echo "🌐 API Gateway: http://localhost:9000"
	@echo "📊 Grafana: http://localhost:3000 (admin/admin)"
	@echo "📈 Prometheus: http://localhost:9090"
	@echo "📋 Kibana: http://localhost:5601"
	@echo "🐰 RabbitMQ: http://localhost:15672 (admin/password)"

