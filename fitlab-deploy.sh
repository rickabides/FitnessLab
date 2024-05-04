#!/bin/bash

# Build the Docker image and tag it
docker build -t fitlab . && echo "Docker build successful." || { echo "Docker build failed."; exit 1; }

# Submit the Docker image to Google Cloud Build
gcloud builds submit --tag gcr.io/mlcclab-419521/fitlab && echo "Cloud build successful." || { echo "Cloud build failed."; exit 1; }

# Deploy the Docker image on Google Cloud Run specifying the region
gcloud run deploy fitlab --image gcr.io/mlcclab-419521/fitlab --region us-west1 --allow-unauthenticated && echo "Deployment successful." || { echo "Deployment failed."; exit 1; }

echo "All operations completed successfully."

