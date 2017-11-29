#!/usr/bin/env bash

set -ex

IMAGE=dq-worker
VERSION=`git rev-parse --short HEAD`
echo "version: $VERSION"

docker build -t gcr.io/dist-queue/${IMAGE}:${VERSION} -f ../docker/Dockerfile ..