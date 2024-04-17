#!/bin/bash

if [[ $1 == "dev" ]]; then

    echo "Installing dependencies..."
    pip install -r backend/CloudRun-base/requirements.txt
    
    export PORT=8080
    echo "Building development images..."
    docker-compose -f docker-compose.dev.yaml build

elif [[ $1 == "prod" ]]; then

    echo "Installing dependencies..."
    pip install -r backend/CloudRun-base/requirements.txt
    
    export PORT=8080
    echo "Building development images..."
    docker-compose -f docker-compose.prod.yaml build

else
    echo "Invalid or no flag provided. Please use 'dev' or 'prod'."
    exit 1
fi