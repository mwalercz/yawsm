#!/usr/bin/env bash

set -ex

IMAGE=yawsm
VERSION=`git rev-parse --short HEAD`
echo "version: $VERSION"

docker build -t gcr.io/dist-queue/${IMAGE}:${VERSION} -f ../docker/Dockerfile ..