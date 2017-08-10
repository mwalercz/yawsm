#!/usr/bin/env bash

CMD="$1"
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
HOST="$2"

function generate_keys {
        if [ -d "$KEYS_DIR" ]; then
            rm ${KEYS_DIR} -rf
        fi
        mkdir ${KEYS_DIR}
        openssl genrsa -out ${KEYS_DIR}/server.key 2048
        openssl rsa -in ${KEYS_DIR}/server.key -out ${KEYS_DIR}/server.key
        openssl req -sha256 -new -key ${KEYS_DIR}/server.key -out ${KEYS_DIR}/server.csr -subj "/CN=$1"
        echo subjectAltName = DNS:$1,IP:10.10.10.20,IP:127.0.0.1 > extfile.cnf
        openssl x509 -req -sha256 -days 365 -in ${KEYS_DIR}/server.csr \
        -signkey ${KEYS_DIR}/server.key -out ${KEYS_DIR}/server.crt -extfile extfile.cnf
        rm extfile.cnf
}

case ${CMD} in
    postgres-up)
        docker-compose -f ${DOCKER_DIR}/docker-compose.yml up -d postgres ;;
    up)
        docker-compose -f ${DOCKER_DIR}/docker-compose.yml up -d  ;;
    down)
        docker-compose -f ${DOCKER_DIR}/docker-compose.yml down ;;
    tests)
        docker-compose -f ${DOCKER_DIR}/docker-compose.yml -f \
        ${DOCKER_DIR}/docker-compose.yml up tests ;;
    generate_keys)
        generate_keys ${HOST} ;;
    *)
        echo "Command '$CMD' does not exist" ;;
esac

