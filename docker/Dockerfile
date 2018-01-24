FROM python:3.6.1-alpine

RUN apk update \
    && apk add gcc libffi-dev openssl openssl-dev python3-dev \
    musl-dev postgresql-dev make openssh ca-certificates \
    bash curl

ENV YAWSM_DATABASE_NAME=yawsm \
    YAWSM_DATABASE_USER=yawsm \
    YAWSM_DATABASE_PASSWORD=yawsm

# python
WORKDIR /usr/src/app
COPY requirements.txt .
COPY requirements_dev.txt .
COPY setup.py .
RUN pip install -e . \
&& pip install -r requirements_dev.txt

#others
COPY ./docker/entrypoint.sh /usr/bin/entrypoint
COPY ./bin/dq.sh /usr/bin/dq
RUN chmod 755 /usr/bin/entrypoint \
&& chmod 755 /usr/bin/dq
RUN dq generate_keys localhost \
&& ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa \
&& ssh-keygen -f /etc/ssh/ssh_host_dsa_key -N '' -t dsa \
&& mkdir -p /var/run/sshd \
&& adduser -S test -s /bin/bash \
&& echo 'test:test' | chpasswd \
&& adduser -S admin -s /bin/bash \
&& echo 'admin:admin' | chpasswd

COPY . .

ENTRYPOINT ["entrypoint"]



