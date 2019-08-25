# from .celery import app as celery_app


from __future__ import absolute_import
from blog_run.celery import app as celery_app

import pymysql
pymysql.install_as_MySQLdb()

