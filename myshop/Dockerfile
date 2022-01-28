FROM python:3.8.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/online_shop
WORKDIR /usr/src/online_shop

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/online_shop
RUN pip install -r requirements.txt

COPY . /usr/src/online_shop

EXPOSE 8000
CMD ["python", "manage.py","runserver","0.0.0.0:8000"]