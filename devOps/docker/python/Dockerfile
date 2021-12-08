FROM python:3.8

COPY ./ /var/www/project

RUN python -m pip install pipenv && pipenv install


# Set timezone
RUN rm /etc/localtime
RUN ln -s /usr/share/zoneinfo/Europe/Berlin /etc/localtime
RUN "date"

WORKDIR /var/www/project

CMD FLASK_ENV=development python app.py