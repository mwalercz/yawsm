#!/usr/bin/env bash

set -ex
USERNAME=mwalercz
IMAGE=dq_broker
docker build -t ${USERNAME}/${IMAGE}:latest -f docker/Dockerfile .