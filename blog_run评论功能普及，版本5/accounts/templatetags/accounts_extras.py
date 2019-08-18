from datetime import datetime

from django import template

register = template.Library()

def datefmt(value):
    print(type(value))
    # for i in value:
    #     if i in ['年','月','日']:
    #         value.replace(i, '-')
    return value


register.filter('datefmt',datefmt)
