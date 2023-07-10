ARG PIP_DOWNLOAD_CACHE=/.cache/pip
FROM ubuntu:20.04
COPY ci/docker/python/linux/tox/apt-packages.txt /tmp/
RUN apt update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    cat /tmp/apt-packages.txt | xargs apt-get -y install
ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL

COPY requirements/ /tmp/requirements
RUN python3 -m pip install pip --upgrade && \
    python3 -m pip install wheel && \
    python3 -m pip install -r /tmp/requirements/requirements_tox.txt devpi-client && \
    python3 -m pip wheel -w wheels wheel

ARG PIP_DOWNLOAD_CACHE
RUN mkdir -p ${PIP_DOWNLOAD_CACHE} && \
    chmod -R 777 ${PIP_DOWNLOAD_CACHE}

WORKDIR /src
CMD tox --workdir /tmp/tox --recreate
