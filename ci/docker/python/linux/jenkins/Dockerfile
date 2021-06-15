ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION} as wheel_builder

ADD requirements.txt ci/docker/python/shared/requirements-ci.txt /tmp/
ARG PYTHON_INDEX=https://devpi.library.illinois.edu/production/release
RUN python -m pip install --upgrade pip &&  \
    pip install setuptools && \
    pip install wheel && \
    pip wheel --wheel-dir=/wheels \
        -r /tmp/requirements.txt \
        -r /tmp/requirements-ci.txt

FROM python:${PYTHON_VERSION}
ARG USER_ID=1000
ARG GROUP_ID=1000

RUN groupadd -g $GROUP_ID user && \
    useradd -u $USER_ID -s /bin/sh -m -d /home/user -g user user

RUN mkdir -p /.cache/pip && \
    chmod -R 777 /.cache

ENV SONAR_SCANNER_VERSION=4.4.0.2170
ARG SONAR_SCANNER_HOME=/opt/sonar/${SONAR_SCANNER_VERSION}-linux
ENV SONAR_USER_HOME=/opt/sonar/.sonar
RUN curl --create-dirs -sSLo /tmp/sonar-scanner.zip \
        https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-$SONAR_SCANNER_VERSION-linux.zip && \
    unzip -o /tmp/sonar-scanner.zip -d /opt/sonar/ && \
    rm /tmp/sonar-scanner.zip && \
    mkdir -p $SONAR_USER_HOME/cache && \
    chmod -R 777 "${SONAR_USER_HOME}" &&\
    mkdir -p /home/user/.sonar/cache && \
    chown user:user /home/user/.sonar/cache && \
    ln -s /opt/sonar/sonar-scanner-$SONAR_SCANNER_VERSION-linux/bin/sonar-scanner /usr/local/bin/sonar-scanner
ENV SONAR_SCANNER_OPTS="-server"

COPY --from=wheel_builder /wheels /wheels/
ADD requirements.txt ci/docker/python/shared/requirements-ci.txt /tmp/
ARG PIP_EXTRA_INDEX_URL
ARG PIP_TRUSTED_HOST
RUN python -m pip install --upgrade pip &&  \
    pip install setuptools && \
    pip install wheel && \
    pip install --no-index --find-links=/wheels \
        -r /tmp/requirements.txt \
        -r /tmp/requirements-ci.txt
RUN pip install types-PyYAML
RUN pip install devpi-client
ENV PIP_FIND_LINKS=/wheels
USER user
WORKDIR /home/user