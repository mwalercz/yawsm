FROM quozd/centos7-python36
COPY .. /app
WORKDIR /app
COPY ./docker/entrypoint.sh /usr/bin/entrypoint
RUN yum install yum install postgresql-libs && \
    chmod 755 /usr/bin/entrypoint

ENTRYPOINT ["entrypoint.sh"]



