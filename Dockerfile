FROM python:3.8
USER root


RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
RUN apt-get install -y vim less

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN mkdir -p /root/app
COPY requirements.txt /root/app
WORKDIR /root/app

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN python -m pip install jupyterlab
RUN pip install -r requirements.txt

EXPOSE 8501
