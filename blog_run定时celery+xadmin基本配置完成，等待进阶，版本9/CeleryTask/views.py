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
from .tasks import run_test_suit


# def tasks(request):
#     print('before run_test_suit')
#     run_test_suit.delay('110')
#     print('after run_test_suit')
#     return HttpResponse("job is runing background~")