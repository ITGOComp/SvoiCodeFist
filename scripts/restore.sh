#!/bin/bash

# Restore script for microservices databases

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <backup_file.tar.gz>"
    echo "Example: $0 backup_20240101_120000.tar.gz"
    exit 1
fi

BACKUP_FILE=$1

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file $BACKUP_FILE not found"
    exit 1
fi

echo "🔄 Starting database restore from $BACKUP_FILE..."

# Extract backup
TEMP_DIR=$(mktemp -d)
tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"

# List of databases to restore
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

# Function to restore database
restore_database() {
    local container=$1
    local database=$2
    local backup_file="$TEMP_DIR/${database}.sql.gz"
    
    if [ ! -f "$backup_file" ]; then
        echo "⚠️  Backup file for $database not found, skipping..."
        return 0
    fi
    
    echo "Restoring $database to $container..."
    
    # Drop and recreate database
    docker-compose exec -T "$container" psql -U user -c "DROP DATABASE IF EXISTS $database;"
    docker-compose exec -T "$container" psql -U user -c "CREATE DATABASE $database;"
    
    # Restore from backup
    gunzip -c "$backup_file" | docker-compose exec -T "$container" psql -U user -d "$database"
    
    if [ $? -eq 0 ]; then
        echo "✅ $database restored successfully"
    else
        echo "❌ Failed to restore $database"
    fi
}

# Restore all databases
for db_info in "${databases[@]}"; do
    container=$(echo $db_info | cut -d: -f1)
    database=$(echo $db_info | cut -d: -f2)
    restore_database "$container" "$database"
done

# Restore Redis data
if [ -f "$TEMP_DIR/redis.rdb" ]; then
    echo "Restoring Redis data..."
    docker-compose stop redis
    docker cp "$TEMP_DIR/redis.rdb" "$(docker-compose ps -q redis):/data/dump.rdb"
    docker-compose start redis
    echo "✅ Redis data restored successfully"
fi

# Cleanup
rm -rf "$TEMP_DIR"

echo "✅ Restore completed successfully!"
echo "🔄 Restarting services..."
docker-compose restart

echo "✅ All services restarted!"

