FROM python:3.6.8

WORKDIR /workspace
ADD . /workspace

RUN pip install pipenv
RUN pipenv install --deploy --system


# vi:et:ts=2:sw=2:cc=80
