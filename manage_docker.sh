#!/bin/zsh

COMPOSE_FILE="./docker-compose-dev.yaml"

up_services() {
    echo "Starting services..."
    docker-compose -f $COMPOSE_FILE up -d
}

down_services() {
    echo "Removing services..."
    docker-compose -f $COMPOSE_FILE down
}

restart_services() {
    echo "Restarting services..."
    down_services
    up_services
}

if [ ! -f "$COMPOSE_FILE" ]; then
    echo "Docker compose file not found!"
    exit 1
fi


# Main menu
case $1 in
    up)
        up_services
        ;;
    down)
        down_services
        ;;
    restart)
        restart_services
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac

exit 0
