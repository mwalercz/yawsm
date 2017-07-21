FROM python:3.6.1-alpine

RUN apk update \
    && apk add gcc libffi-dev openssl openssl-dev python3-dev \
    musl-dev postgresql-dev make openssh ca-certificates \
    bash curl

ENV BROKER_DATABASE_NAME=dq_broker \
    BROKER_DATABASE_USER=dq_broker \
    BROKER_DATABASE_PASSWORD=dq_broker

# python
RUN mkdir -p /usr/src/app
COPY requirements.txt /usr/src/app/
COPY requirements_dev.txt /usr/src/app/
COPY . /usr/src/app
WORKDIR /usr/src/app
COPY ./docker/entrypoint.sh /usr/bin/entrypoint
COPY ./bin/dq.sh /usr/bin/dq
RUN chmod 755 /usr/bin/entrypoint \
&& chmod 755 /usr/bin/dq
RUN ["dq", "generate_keys"]

# ssh
RUN ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa \
&& 	ssh-keygen -f /etc/ssh/ssh_host_dsa_key -N '' -t dsa \
&&  mkdir -p /var/run/sshd

# user
RUN adduser -S test -s /bin/bash
RUN echo 'test:test' | chpasswd

RUN pip install -e . \
&& pip install -r requirements_dev.txt

ENTRYPOINT ["entrypoint"]



