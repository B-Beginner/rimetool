#!/bin/bash
# Create and use a builder instance (if not already created)
docker buildx create --use --name mybuilder || docker buildx use mybuilder

# Build the image for linux/arm64/v8 and push it to Docker Hub
docker buildx build --platform linux/arm64/v8  -t whitewatercn/rimetool:arm64 --push .
