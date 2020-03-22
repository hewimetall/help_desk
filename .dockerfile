FROM python:3.8
ENV PYTHONUNBUFFERED 1
#   wsgi setting (dev or prod)
ENV DJANGO_ENV dev 
# env for create Superuser in django
ENV DJANGO_SUPERUSER_PASSWORD x
ENV DJANGO_SUPERUSER_USERNAME x
ENV DJANGO_SUPERUSER_EMAIL x@xer.com

RUN mkdir /code
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . /code/

#setting django
RUN python manage.py makemigrations 
RUN python manage.py migrate
RUN python manage.py collectstatic --no-input --clear
RUN python manage.py createsuperuser --noinput  --username ${DJANGO_SUPERUSER_USERNAME} --email ${DJANGO_SUPERUSER_EMAIL} 
RUN bash -c ls
CMD gunicorn core.wsgi --bind 0.0.0.0:80
# CMD bash