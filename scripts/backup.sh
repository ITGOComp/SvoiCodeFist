#!/bin/bash

# Backup script for microservices databases

set -e

BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "💾 Starting database backup to $BACKUP_DIR..."

# List of databases to backup
databases=(
    "user-db:user_service"
    "incident-db:incident_service"
    "traffic-db:traffic_service"
    "news-db:news_service"
    "chat-db:chat_service"
    "analytics-db:analytics_service"
    "traffic-analytics-db:traffic_analytics_service"
    "schedule-db:schedule_service"
    "notification-db:notification_service"
)

# Function to backup database
backup_database() {
    local container=$1
    local database=$2
    local backup_file="$BACKUP_DIR/${database}.sql"
    
    echo "Backing up $database from $container..."
    
    docker-compose exec -T "$container" pg_dump -U user -d "$database" > "$backup_file"
    
    if [ $? -eq 0 ]; then
        echo "✅ $database backed up successfully"
        # Compress backup
        gzip "$backup_file"
    else
        echo "❌ Failed to backup $database"
        rm -f "$backup_file"
    fi
}

# Backup all databases
for db_info in "${databases[@]}"; do
    container=$(echo $db_info | cut -d: -f1)
    database=$(echo $db_info | cut -d: -f2)
    backup_database "$container" "$database"
done

# Backup Redis data
echo "Backing up Redis data..."
docker-compose exec -T redis redis-cli --rdb - > "$BACKUP_DIR/redis.rdb"

# Create backup archive
echo "Creating backup archive..."
cd "$BACKUP_DIR"
tar -czf "../backup_$(date +%Y%m%d_%H%M%S).tar.gz" .
cd ..
rm -rf "$BACKUP_DIR"

echo "✅ Backup completed successfully!"
echo "📁 Backup file: backup_$(date +%Y%m%d_%H%M%S).tar.gz"

