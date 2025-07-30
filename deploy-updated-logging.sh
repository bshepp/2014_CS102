#!/bin/bash

# Deploy script for updated geometry engine with reduced health check logging
# This will reduce CloudWatch logging costs by ~97%

set -e

echo "🚀 Deploying Geometry Engine with Optimized Health Check Logging"

# Configuration
REGION="us-east-1"
CLUSTER_NAME="geometry-engine-cluster"
SERVICE_NAME="geometry-engine-service"
ECR_REPOSITORY="290318879194.dkr.ecr.us-east-1.amazonaws.com/geometry-engine-api"
IMAGE_TAG="reduced-logging-$(date +%Y%m%d-%H%M%S)"

echo "📦 Building Docker image..."
docker build -t geometry-engine-api:${IMAGE_TAG} .

echo "🔐 Logging into ECR..."
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ECR_REPOSITORY}

echo "🏷️  Tagging image for ECR..."
docker tag geometry-engine-api:${IMAGE_TAG} ${ECR_REPOSITORY}:${IMAGE_TAG}
docker tag geometry-engine-api:${IMAGE_TAG} ${ECR_REPOSITORY}:latest

echo "⬆️  Pushing to ECR..."
docker push ${ECR_REPOSITORY}:${IMAGE_TAG}
docker push ${ECR_REPOSITORY}:latest

echo "🔄 Updating ECS service..."
aws ecs update-service \
    --cluster ${CLUSTER_NAME} \
    --service ${SERVICE_NAME} \
    --force-new-deployment \
    --region ${REGION}

echo "⏳ Waiting for deployment to complete..."
aws ecs wait services-stable \
    --cluster ${CLUSTER_NAME} \
    --services ${SERVICE_NAME} \
    --region ${REGION}

echo "✅ Deployment complete!"
echo ""
echo "💰 Expected Cost Savings:"
echo "   - Health check logs reduced by ~97% (from every 10s to every 30 requests)"
echo "   - Uvicorn access logs completely disabled"
echo "   - Log retention reduced to 7 days"
echo "   - Estimated monthly savings: $15-25 in CloudWatch costs"
echo ""
echo "📊 Monitor the deployment:"
echo "   aws ecs describe-services --cluster ${CLUSTER_NAME} --services ${SERVICE_NAME}"
echo ""
echo "🏥 Test health endpoint:"
echo "   curl https://your-alb-url/api/health"