#!/bin/bash

set -e

IMAGE_NAME=$1

# If tag is empty, then throw an error and stop

if [ -z "$IMAGE_NAME" ]; then
    echo "Please provide a image name and tag"
    exit 1
fi

git archive -v -o __api.tar.gz --format=tar.gz HEAD
docker build -t $IMAGE_NAME -f Dockerfile .
