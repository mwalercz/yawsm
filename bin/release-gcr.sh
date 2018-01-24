#!/usr/bin/env bash

set -ex

IMAGE=yawsm
VERSION=`git rev-parse --short HEAD`
echo "version: $VERSION"

./build-gcr.sh
gcloud docker -- push gcr.io/dist-queue/${IMAGE}:${VERSION}