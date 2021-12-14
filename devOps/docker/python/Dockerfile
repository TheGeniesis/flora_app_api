FROM python:3.8-slim-buster

COPY ./ /var/www/project
WORKDIR /var/www/project

RUN python -m pip install pipenv && pipenv install --deploy --ignore-pipfile

# Set timezone
RUN rm /etc/localtime
RUN ln -s /usr/share/zoneinfo/Europe/Berlin /etc/localtime
RUN "date"

CMD ["pipenv", "run", "python", "app.py"]
