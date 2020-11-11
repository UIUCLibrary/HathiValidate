# escape=`
ARG PYTHON_VERSION=3.7
ARG PYTHON_DOCKER_IMAGE_BASE=python:${PYTHON_VERSION}
FROM ${PYTHON_DOCKER_IMAGE_BASE} as wheel_builder
ADD requirements.txt ci/docker/python/shared/requirements-ci.txt c:/tmp/
RUN python -m pip install --upgrade pip ; `
    pip install --upgrade setuptools ; `
    pip install wheel

RUN pip wheel --wheel-dir=c:/wheels `
    -r c:/tmp/requirements.txt `
    -r c:/tmp/requirements-ci.txt

FROM ${PYTHON_DOCKER_IMAGE_BASE}

RUN certutil -generateSSTFromWU roots.sst ; certutil -addstore -f root roots.sst ; del roots.sst


COPY --from=wheel_builder c:/wheels c:/wheels/
ADD requirements.txt ci/docker/python/shared/requirements-ci.txt c:/tmp/
ENV PIP_EXTRA_INDEX_URL="https://devpi.library.illinois.edu/production/release"
ENV PIP_TRUSTED_HOST="devpi.library.illinois.edu"

RUN pip install --no-index --find-links=c:/wheels -r c:/tmp/requirements.txt -r c:/tmp/requirements-ci.txt
ENV PIP_FIND_LINKS=c:/wheels