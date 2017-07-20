#!/usr/bin/env bash

ARG="$1"
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ ${SOURCE} != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
ROOT_DIR=${DIR}/..
DOCKER_DIR=${ROOT_DIR}/docker
KEYS_DIR=${ROOT_DIR}/keys

case ${ARG} in
    postgres-exposed-up)
        docker-compose -f ${DOCKER_DIR}/docker-compose.postgres-exposed.yml up -d postgres ;;
    postgres-exposed-down)
        docker-compose -f ${DOCKER_DIR}/docker-compose.postgres-exposed.yml down ;;
    tests)
        docker-compose -f ${DOCKER_DIR}/docker-compose.yml -f \
        ${DOCKER_DIR}/docker-compose.override.yml up tests ;;
    generate_keys)
        if [ -d "$KEYS_DIR" ]; then
            rm ${KEYS_DIR} -rf
        fi
        mkdir ${KEYS_DIR}
        openssl genrsa -out ${KEYS_DIR}/server.key 2048
        openssl rsa -in ${KEYS_DIR}/server.key -out ${KEYS_DIR}/server.key
        openssl req -sha256 -new -key ${KEYS_DIR}/server.key -out ${KEYS_DIR}/server.csr -subj '/CN=localhost'
        openssl x509 -req -sha256 -days 365 -in ${KEYS_DIR}/server.csr -signkey ${KEYS_DIR}/server.key -out ${KEYS_DIR}/server.crt
        ;;
    *)
        echo "Command '$ARG' does not exist" ;;
esac
