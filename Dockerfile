FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /dependencies
ADD ./dependencies/apt_requirements.txt /dependencies
ADD ./dependencies/dev_requirements.txt /dependencies
RUN pip install --upgrade pip
RUN apt-get update &&\
    apt-get install -y $(cat /code/dependencies/apt_requirements.txt) || exit 1
RUN pip install -r /dependencies/dev_requirements.txt
RUN mkdir /code;
WORKDIR /code
ADD ./ /code
RUN mkdir /code/core/static;
RUN mkdir /code/core/static/webpack_bundles;
RUN python manage.py collectstatic --noinput
RUN apt-get clean
# Node installation
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get update && apt-get install -y \
    nodejs
#RUN npm install && npm run production