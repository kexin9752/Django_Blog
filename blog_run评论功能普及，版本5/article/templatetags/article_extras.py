from datetime import datetime

from django import template

from article.models import Article

register = template.Library()

def content_len(value):
    if len(value) > 111:
        value = value[:110]
    return value


register.filter('content_len',content_len)
