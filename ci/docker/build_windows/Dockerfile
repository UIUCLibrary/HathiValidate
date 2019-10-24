# escape=`

FROM python:3.7
RUN certutil -generateSSTFromWU roots.sst ; certutil -addstore -f root roots.sst ; del roots.sst
ADD requirements.txt c:\temp\requirements.txt
RUN python -m pip install pip --upgrade ; pip install --no-cache-dir sphinx tox pytest-runner mypy lxml pytest pytest-cov flake8 -r c:\temp\requirements.txt