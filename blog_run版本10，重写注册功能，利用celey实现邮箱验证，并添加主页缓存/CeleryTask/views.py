from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
# from CeleryTask.tasks import test
#
#
# def test_run(request):
#     test.delay(2,3)
#     return JsonResponse({'status':'ok'})


from django.http import HttpResponse
from .tasks import email_send


def tasks_test(request):
    print('before run_test_suit')
    email_send.delay('110')
    print('after run_test_suit')
    return HttpResponse("job is runing background~")

