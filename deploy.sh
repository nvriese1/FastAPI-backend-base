#!/bin/bash

if [[ $1 == "dev" ]]; then

    echo "Running in development mode..."
    export LOCAL_DEPLOYMENT=true
    export PORT=8080

    docker-compose -f docker-compose.dev.yaml down
    docker-compose -f docker-compose.dev.yaml up -d

elif [[ $1 == "prod" ]]; then

    echo "Running in production mode..."
    export LOCAL_DEPLOYMENT=false
    export PORT=8080
    
    docker-compose -f docker-compose.prod.yaml down
    docker-compose -f docker-compose.prod.yaml up -d

else
    echo "Invalid or no flag provided. Please use 'dev' or 'prod'."
    exit 1
fi