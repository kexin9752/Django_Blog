from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect, render

from accounts.models import User


# def ip_middleware(get_response):
#
#     def middleware(request):
#         ip = request.META.get('REMOTE_ADDR',None)
#         print(ip)
#         ip_disable_list = [
#             '127.0.0.1'
#         ]
#         if ip in ip_disable_list:
#             return HttpResponse('ip is forbid')
#         response = get_response(request)
#         print('456')
#         return response
#     return middleware


class AccountsAuthMiddleware(object):

    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request, *args, **kwargs):
        ret_url = request.get_full_path()
        if ret_url[1:9] == 'accounts' and ret_url != '/accounts/user/login/' and ret_url[:22] != '/accounts/verify/code/':
            user = request.user
            if user.is_anonymous:
                return render(request,'error.html')
        response = self.get_response(request)
        return response


