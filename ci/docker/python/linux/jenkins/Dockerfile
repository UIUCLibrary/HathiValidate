ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION} as base
FROM base as wheel_builder

ADD requirements.txt ci/docker/python/shared/requirements-ci.txt /tmp/
COPY requirements/*.txt /tmp/requirements/
RUN python -m pip install --upgrade pip &&  \
    pip install setuptools && \
    pip install wheel && \
    pip wheel --wheel-dir=/wheels \
        -r /tmp/requirements.txt \
        -r /tmp/requirements-ci.txt

FROM base

RUN mkdir -p /.cache/pip && \
    chmod -R 777 /.cache

ENV SONAR_SCANNER_VERSION=4.7.0.2747
ARG SONAR_SCANNER_HOME=/opt/sonar/${SONAR_SCANNER_VERSION}-linux
ENV SONAR_USER_HOME=/opt/sonar/.sonar

RUN curl --create-dirs -sSLo /tmp/sonar-scanner.zip \
        https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-$SONAR_SCANNER_VERSION-linux.zip && \
    unzip -o /tmp/sonar-scanner.zip -d /opt/sonar/ && \
    rm /tmp/sonar-scanner.zip && \
    mkdir -p $SONAR_USER_HOME/cache && \
    chmod -R 777 "${SONAR_USER_HOME}" &&\
    ln -s /opt/sonar/sonar-scanner-$SONAR_SCANNER_VERSION-linux/bin/sonar-scanner /usr/local/bin/sonar-scanner && \
    which sonar-scanner

ENV SONAR_SCANNER_OPTS="-server"

COPY --from=wheel_builder /wheels /wheels/
ADD requirements.txt ci/docker/python/shared/requirements-ci.txt /tmp/
COPY requirements/*.txt /tmp/requirements/
ARG PIP_EXTRA_INDEX_URL
ARG PIP_TRUSTED_HOST
ENV PIP_FIND_LINKS=/wheels
RUN python -m pip install --upgrade pip &&  \
    pip install setuptools && \
    pip install wheel && \
    pip install --no-index --find-links=/wheels \
        -r /tmp/requirements.txt \
        -r /tmp/requirements-ci.txt
