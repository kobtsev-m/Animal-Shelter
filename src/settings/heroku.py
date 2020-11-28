from .base import *

import dj_database_url
import os


SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False

ALLOWED_HOSTS = ['frozen-springs-02490.herokuapp.com']

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')