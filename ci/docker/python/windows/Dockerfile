# escape=`
ARG PYTHON_DOCKER_IMAGE_BASE=python:3.7
FROM ${PYTHON_DOCKER_IMAGE_BASE}

RUN certutil -generateSSTFromWU roots.sst ; certutil -addstore -f root roots.sst ; del roots.sst
ADD requirements.txt ci/docker/python/shared/requirements-ci.txt c:/tmp/

RUN python -m pip install --upgrade pip ; `
    pip install --upgrade setuptools ; `
    pip install wheel

RUN pip wheel --wheel-dir=/wheels `
    -r c:/tmp/requirements.txt `
    -r c:/tmp/requirements-ci.txt `
RUN tox --version