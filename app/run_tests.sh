#!/bin/bash

export SECRET_KEY=foobar
export DJANGO_ALLOWED_HOSTS=*
export EMAIL_HOST_USER="will@testing.com"
export EMAIL_HOST_PASSWORD="aldshlaiejclkdjvaia!29zoioae"
python manage.py test tests
