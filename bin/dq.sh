#!/usr/bin/env bash

ARG="$1"
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ ${SOURCE} != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
DOCKER_DIR=${DIR}/../docker

case ${ARG} in
    postgres-exposed-up)
        docker-compose -f ${DOCKER_DIR}/docker-compose.postgres-exposed.yml up -d postgres ;;
    postgres-exposed-down)
        docker-compose -f ${DOCKER_DIR}/docker-compose.postgres-exposed.yml down ;;
    tests)
        docker-compose -f ${DOCKER_DIR}/docker-compose.yml -f \
        ${DOCKER_DIR}/docker-compose.override.yml up tests ;;
    *)
        echo "Command '$ARG' does not exist" ;;
esac
